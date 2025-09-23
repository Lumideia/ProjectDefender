from typing import Dict, Tuple, Optional, TYPE_CHECKING, List

import pygame

from src.enteties.character_instance import CharacterInstance
from src.rules.perks.perk import Perk
from src.rules.perks.registry import create_perk

from src.ui.theme import COLORS

if TYPE_CHECKING:
    from src.ui.perks_screen.perk_screen import PerkScreen


class PerkTile:
    """Один тайл с перком в гриде."""

    def __init__(self, perk: Perk, rect: pygame.Rect, screen: "PerkScreen", row_index: int):
        self.perk = perk
        self.rect = rect
        self.screen = screen
        self.row_index = row_index
        self.hovered = False
        self.selected = False

    @staticmethod
    def perk_color(perk: Perk):
        if perk.is_taken is None:
            return COLORS['NOT_TAKEN']
        if not perk.is_taken:
            return COLORS['CANCELED']
        if perk.is_completed:
            return COLORS['COMPLETED']
        if not perk.is_activated:
            return COLORS['PASSIVE']
        if not perk.could_be_activated(perk.owner):
            return COLORS['COOLDOWN']
        return COLORS['READY']

    def draw(self, surface: pygame.Surface):
        color = self.perk_color(self.perk)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLORS['FRAME'], self.rect, 2, border_radius=6)
        # название
        title = self.screen._perk_title(self.perk)
        self.screen._blit_wrapped_center(title, self.rect, self.screen.font_cell)

        # cd
        cd_left = getattr(self.perk, "cd_left", 0) or 0
        if cd_left > 0:
            cd = self.screen.font_cd.render(str(f'cd: {cd_left}'), True, COLORS['TEXT'])
            surface.blit(cd, cd.get_rect(bottomright=(self.rect.right - 6, self.rect.bottom - 4)))

        # usages
        uses_left = None
        if hasattr(self.perk, "uses_left"):
            uses_left = self.perk.uses_left
        if uses_left is not None:
            ul = self.screen.font_cd.render(str(f'uses: {uses_left}'), True, COLORS['TEXT'])
            surface.blit(ul, ul.get_rect(bottomleft=(self.rect.left + 6, self.rect.bottom - 4)))

        # special

    def handle_event(self, event: pygame.event.Event, *, double_click: bool):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            if self.hovered:
                self.screen.hovered_perk = self.perk
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.perk.is_taken is not False:
                if double_click:
                    if self.perk.could_be_activated(self.perk.owner) and hasattr(self.perk, "try_trigger"):
                        self.perk.try_trigger(self.perk.owner, None)
                else:
                    self.selected = True
                    if self.perk.is_taken is None:
                        self.perk.owner.activate_perk(self.perk)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.rect.collidepoint(event.pos) and self.perk.is_taken:
                self.perk.tick()


class TileGrid:
    def __init__(self, start_x, start_y, cell_w, cell_h, margin, colors: Dict[str, Tuple[int, int, int]]):
        self.w = 800
        self.start_x, self.start_y = start_x, start_y
        self.cell_w, self.cell_h = cell_w, cell_h
        self.margin = margin
        self.tiles: List[List[PerkTile]] = []
        self.hovered_perk: Optional[Perk] = None
        self.colors = colors

    def rebuild(self, character: CharacterInstance, screen: "PerkScreen"):
        self.tiles = []
        id_to_perk = {p.perk_id: p for p in character.perks}

        for r, row in enumerate(character.perk_order):
            n = len(row)
            cell_w_row = (self.w - self.margin * (n - 1)) // n
            tile_row = []
            for c, pid in enumerate(row):
                x = self.start_x + c * (cell_w_row + self.margin)
                y = self.start_y + r * (self.cell_h + self.margin)
                rect = pygame.Rect(x, y, cell_w_row, self.cell_h)
                tile_row.append(PerkTile(id_to_perk[pid], rect, screen, r))
            self.tiles.append(tile_row)

    def draw(self, surface: pygame.Surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)

    def handle_event(self, event: pygame.event.Event, *, double_click: bool):
        for row in self.tiles:
            for tile in row:
                tile.handle_event(event, double_click=double_click)
                if tile.hovered:
                    self.hovered_perk = tile.perk
