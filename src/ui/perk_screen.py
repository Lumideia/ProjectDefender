import pygame
from typing import Dict, List, Tuple, Optional

from src.constant.world import WORLD_BUS
from src.enteties.character_instance import Grenadier
from src.rules.events.types import Event, EventCtx
from src.rules.perks.registry import create_perk
from src.rules.perks.perk import Perk

# --- загрузка текстов перков ---
from src.rules.perks.description.active import ACTIVE_PERKS
from src.rules.perks.description.aura import AURA_PERKS
from src.rules.perks.description.one_time import ONE_TIME_PERKS
from src.rules.perks.description.passive import PASSIVE_PERKS

def _merge_titles() -> Dict[int, str]:
    d: Dict[int, str] = {}
    for src in (ONE_TIME_PERKS, PASSIVE_PERKS, ACTIVE_PERKS, AURA_PERKS):
        try:
            d.update({pid: meta["title"] for pid, meta in src.items()})
        except Exception:
            pass
    return d

def _merge_descs() -> Dict[int, str]:
    d: Dict[int, str] = {}
    for src in (ONE_TIME_PERKS, PASSIVE_PERKS, ACTIVE_PERKS, AURA_PERKS):
        try:
            d.update({pid: meta["description"] for pid, meta in src.items()})
        except Exception:
            pass
    return d

UI_TITLES: Dict[int, str] = _merge_titles()
UI_DESCS:  Dict[int, str] = _merge_descs()


# ======================================================================
#   UI-элементы
# ======================================================================

class PerkTile:
    """Один тайл с перком в гриде."""
    def __init__(self, perk: Perk, rect: pygame.Rect, screen: "PerkScreen", row_index: int):
        self.perk = perk
        self.rect = rect
        self.screen = screen
        self.row_index = row_index
        self.hovered = False
        self.selected = False

    def draw(self, surface: pygame.Surface):
        color = self.screen._perk_color(self.perk)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.screen.COLOR_FRAME, self.rect, 2, border_radius=6)
        # название
        title = self.screen._perk_title(self.perk)
        self.screen._blit_wrapped_center(title, self.rect, self.screen.font_cell)
        # кулдаун
        cd_left = getattr(self.perk, "cd_left", 0) or 0
        if cd_left > 0:
            cd = self.screen.font_cd.render(str(cd_left), True, self.screen.COLOR_TEXT)
            surface.blit(cd, cd.get_rect(bottomright=(self.rect.right-6, self.rect.bottom-4)))

    def handle_event(self, event: pygame.event.Event, *, double_click: bool):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            if self.hovered:
                self.screen.hovered_perk = self.perk
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.perk.is_taken:
                if double_click and hasattr(self.perk, "try_trigger"):
                    self.perk.try_trigger(self.screen.character, None)
                else:
                    self.selected = True
                    if self.row_index:  # 0-row always active
                        self.screen.block_row(self.row_index, self)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.rect.collidepoint(event.pos) and self.perk.is_taken:
                self.perk.tick()


# ======================================================================
#   Основной экран
# ======================================================================

class PerkScreen:
    def __init__(self, screen: pygame.Surface, initial: Grenadier):
        self.screen = screen

        # --- шрифты ---
        self.font_title = pygame.font.SysFont("arial", 28, bold=True)
        self.font_cell  = pygame.font.SysFont("arial", 18)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_cd    = pygame.font.SysFont("arial", 22, bold=True)

        # --- layout ---
        self.cell_w, self.cell_h = 210, 84
        self.margin = 12
        self.start_x, self.start_y = 260, 140
        self.sidebar_x, self.sidebar_w = 20, 210
        self.sidebar_item_h = 44

        # --- цвета ---
        self.COLOR_BG         = (10, 10, 20)
        self.COLOR_TEXT       = (220, 220, 220)
        self.COLOR_DIM        = (160, 160, 160)
        self.COLOR_FRAME      = (180, 180, 180)
        self.COLOR_NOT_TAKEN  = (30, 30, 30)
        self.COLOR_PASSIVE = (28, 112, 77)  # было (40, 160, 110)
        self.COLOR_READY = (28, 112, 42)  # было (40, 160, 60)
        self.COLOR_COOLDOWN = (140, 126, 28)  # было (200, 180, 40)
        self.COLOR_BTN        = (60, 60, 60)
        self.COLOR_BTN_HL     = (90, 90, 90)

        # --- верхние кнопки ---
        sw = screen.get_width()
        self.btn_add    = pygame.Rect(sw - 150, 20, 40, 40)
        self.btn_rename = pygame.Rect(sw - 100, 20, 40, 40)
        self.btn_del    = pygame.Rect(sw -  50, 20, 40, 40)

        # список персонажей
        self.characters: List[Tuple[Grenadier, str]] = []
        self.active_idx: int = -1
        self._add_grenadier(initial, name="Grenadier 1")

        self.hovered_perk: Optional[Perk] = None
        self.renaming = False
        self.rename_text = ""
        self.rename_rect = pygame.Rect(sw//2 - 180, 80, 360, 40)

        self._last_click_time = 0
        self._double_click_delay = 400  # ms

        sw, sh = screen.get_size()
        self.btn_end_turn = pygame.Rect(sw - 220, sh - 80, 180, 50)

    # ---------------- персонажи ----------------
    def _add_grenadier(self, grenadier: Grenadier = None, name: str = None):
        g = grenadier or Grenadier()
        nm = name or f"Grenadier {len(self.characters)+1}"
        self.characters.append((g, nm))
        self._activate(len(self.characters)-1)
        self._rebuild_grid()

    def _activate(self, idx: int):
        self.active_idx = max(0, min(idx, len(self.characters)-1))
        self.character, self.character_name = self.characters[self.active_idx]

    def _delete_active(self):
        if not self.characters:
            return
        del self.characters[self.active_idx]
        if not self.characters:
            self._add_grenadier(Grenadier(), "Grenadier 1")
        else:
            self._activate(max(0, self.active_idx-1))
        self._rebuild_grid()

    def _start_rename(self):
        self.renaming = True
        self.rename_text = self.characters[self.active_idx][1]
        try:
            pygame.key.start_text_input()
        except Exception:
            pass

    def _commit_rename(self):
        name = self.rename_text.strip() or self.characters[self.active_idx][1]
        self.characters[self.active_idx] = (self.character, name)
        self.character_name = name
        self.renaming = False
        try:
            pygame.key.stop_text_input()
        except Exception:
            pass

    # ---------------- грид ----------------
    def _rebuild_grid(self):
        """Создаём список объектов PerkTile с готовыми Rect."""
        self.tiles: List[List[PerkTile]] = []
        id_to_perk = {p.perk_id: p for p in self.character.perks}
        # если у персонажа нет перков – создаём
        if not getattr(self.character, "perks", None):
            for row in self.character.perk_order:
                for pid in row:
                    self.character.add_perk(create_perk(pid))
        for r, row in enumerate(self.character.perk_order):
            tile_row: List[PerkTile] = []
            for c, pid in enumerate(row):
                perk = id_to_perk.get(pid)
                x = self.start_x + c * (self.cell_w + self.margin)
                y = self.start_y + r * (self.cell_h + self.margin)
                rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
                tile_row.append(PerkTile(perk, rect, self, r))
            self.tiles.append(tile_row)

    def block_row(self, row_index: int, selected_tile: PerkTile):
        """После выбора одного перка блокируем остальные в ряду."""
        for tile in self.tiles[row_index]:
            if tile is not selected_tile:
                tile.perk.is_taken = False
        selected_tile.perk.is_taken = True

    # ---------------- отрисовка ----------------
    def draw(self):
        self.screen.fill(self.COLOR_BG)
        self._draw_sidebar()
        self._draw_button(self.btn_add, "+")
        self._draw_button(self.btn_rename, "✏")
        self._draw_button(self.btn_del, "🗑")

        # --- новая кнопка внизу ---
        self._draw_button(self.btn_end_turn, "Конец хода")

        # грид
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

        # описание перка при наведении
        if self.hovered_perk:
            self._draw_selected_info(self.hovered_perk)

        if self.renaming:
            self._draw_rename_modal()


    def _draw_sidebar(self):
        area = pygame.Rect(self.sidebar_x, 100, self.sidebar_w, self.screen.get_height()-140)
        pygame.draw.rect(self.screen, (18, 18, 28), area, border_radius=8)
        y = area.y + 10
        for i, (_, name) in enumerate(self.characters):
            rect = pygame.Rect(area.x+10, y, area.width-20, self.sidebar_item_h)
            active = (i == self.active_idx)
            pygame.draw.rect(self.screen, (40, 80, 140) if active else (50, 50, 60), rect, border_radius=6)
            pygame.draw.rect(self.screen, self.COLOR_FRAME, rect, 1, border_radius=6)
            label = self.font_small.render(name, True, self.COLOR_TEXT)
            self.screen.blit(label, (rect.x+10, rect.y+10))
            setattr(self, f"_side_rect_{i}", rect)
            y += self.sidebar_item_h + 10

    def _draw_button(self, rect: pygame.Rect, text: str):
        mx, my = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, self.COLOR_BTN_HL if hovered else self.COLOR_BTN, rect, border_radius=6)
        pygame.draw.rect(self.screen, self.COLOR_FRAME, rect, 1, border_radius=6)
        label = self.font_title.render(text, True, self.COLOR_TEXT)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_selected_info(self, perk: Perk):
        box = pygame.Rect(
            self.start_x,
            self.start_y - 100,
            self.cell_w * len(self.tiles[0]) + self.margin * (len(self.tiles[0]) - 1),
            90
        )
        pygame.draw.rect(self.screen, (18,18,28), box, border_radius=6)
        pygame.draw.rect(self.screen, self.COLOR_FRAME, box, 1, border_radius=6)
        title = self._perk_title(perk)
        desc  = UI_DESCS.get(perk.perk_id, "")
        t1 = self.font_cell.render(title, True, self.COLOR_TEXT)
        self.screen.blit(t1, (box.x+10, box.y+8))
        self._blit_wrapped(desc, (box.x+10, box.y+30), box.width-20, self.font_small, self.COLOR_DIM)

    # ---------------- события ----------------
    def handle_event(self, event: pygame.event.Event):
        double_click = False
        if self.renaming:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._commit_rename()
                elif event.key == pygame.K_ESCAPE:
                    self.renaming = False
                    try:
                        pygame.key.stop_text_input()
                    except Exception:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    self.rename_text = self.rename_text[:-1]
                else:
                    if event.unicode and event.unicode.isprintable():
                        self.rename_text += event.unicode
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            double_click = (now - self._last_click_time) < self._double_click_delay
            self._last_click_time = now

            # --- кнопка конца хода ---
            if self.btn_end_turn.collidepoint(event.pos):
                self._on_end_turn()
                return

            # --- верхние кнопки ---
            if self.btn_add.collidepoint(event.pos):
                self._add_grenadier(Grenadier(), None);
                return
            if self.btn_rename.collidepoint(event.pos):
                self._start_rename();
                return
            if self.btn_del.collidepoint(event.pos):
                self._delete_active();
                return
            for i in range(len(self.characters)):
                r = getattr(self, f"_side_rect_{i}", None)
                if r and r.collidepoint(event.pos):
                    self._activate(i);
                    self._rebuild_grid();
                    return

            # события тайлов
        for row in self.tiles:
            for tile in row:
                tile.handle_event(event, double_click=double_click)

    # ---------------- утилиты ----------------
    def _perk_title(self, perk: Perk) -> str:
        return UI_TITLES.get(perk.perk_id, perk.__class__.__name__)

    def _on_end_turn(self):
        """Вызывается при клике на кнопку 'Конец хода'."""
        # 1. триггерим глобальный ивент конца хода (если используете EventBus)
        try:
            WORLD_BUS.broadcast(Event.TURN_END, EventCtx(Event.TURN_END))
        except Exception:
            # если пока нет реализации EventBus.emit, просто пропустите
            pass

    def _perk_color(self, perk: Perk):
        if not perk.is_taken:
            return self.COLOR_NOT_TAKEN
        if not perk.is_activated:
            return self.COLOR_PASSIVE
        if getattr(perk, "cd_left", 0):
            return self.COLOR_COOLDOWN
        return self.COLOR_READY

    def _blit_wrapped_center(self, text: str, rect: pygame.Rect, font: pygame.font.Font):
        lines = self._wrap_text(text, font, rect.width - 12)
        total_h = len(lines) * font.get_height()
        y = rect.y + (rect.height - total_h)//2
        for ln in lines:
            surf = font.render(ln, True, self.COLOR_TEXT)
            self.screen.blit(surf, surf.get_rect(centerx=rect.centerx, y=y))
            y += font.get_height()

    def _blit_wrapped(self, text: str, pos: Tuple[int,int], max_w: int, font, color):
        x, y = pos
        for ln in self._wrap_text(text, font, max_w):
            self.screen.blit(font.render(ln, True, color), (x, y))
            y += font.get_height()

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        words = text.split()
        lines: List[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    def _draw_rename_modal(self):
        shade = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        shade.fill((0,0,0,160))
        self.screen.blit(shade, (0,0))
        pygame.draw.rect(self.screen, (30,30,40), self.rename_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLOR_FRAME, self.rename_rect, 1, border_radius=8)
        hint = self.font_small.render("Введите имя и нажмите Enter (Esc — отмена)", True, self.COLOR_DIM)
        self.screen.blit(hint, (self.rename_rect.x, self.rename_rect.y - 24))
        txt = self.font_cell.render(self.rename_text, True, self.COLOR_TEXT)
        self.screen.blit(txt, (self.rename_rect.x + 10, self.rename_rect.y + 10))
        cx = self.rename_rect.x + 10 + txt.get_width() + 2
        cy = self.rename_rect.y + 10
        pygame.draw.line(self.screen, self.COLOR_TEXT, (cx, cy), (cx, cy + txt.get_height()), 1)
