import math
import pygame
from typing import Iterable
from src.rules.perks.index import ALL_PERKS
from src.rules.perks.perk import Perk

class AdditionalPerksPanel:
    def __init__(self, parent, rect: pygame.Rect, perks: Iterable[Perk]):
        self.parent = parent
        self.rect = rect
        self.perks = list(perks)
        self.font = pygame.font.SysFont("arial", 18)
        self.active = False

        # настройки таблицы
        self.cols = 5
        self.cell_h = 30
        self.cell_gap = 8
        # ширина колонки с учётом отступов
        self.cell_w = (self.rect.width - (self.cols + 1) * self.cell_gap) // self.cols

    def open(self):
        self.active = True
        self.parent.active_modal = self

    def close(self):
        self.active = False
        if self.parent.active_modal is self:
            self.parent.active_modal = None

    def draw(self, screen: pygame.Surface, character):
        if not self.active:
            return

        pygame.draw.rect(screen, (18,18,28), self.rect, border_radius=8)
        pygame.draw.rect(screen, (200,200,200), self.rect, 1, border_radius=8)

        mouse_pos = pygame.mouse.get_pos()
        # смещаем таблицу по скроллу
        start_y = self.rect.y + self.cell_gap

        for i, perk in enumerate(self.perks):
            row = i // self.cols
            col = i % self.cols

            x = self.rect.x + self.cell_gap + col * (self.cell_w + self.cell_gap)
            y = start_y + row * (self.cell_h + self.cell_gap)
            cell_rect = pygame.Rect(x, y, self.cell_w, self.cell_h)

            # рисуем ячейку, только если она попадает в видимую область
            if self.rect.colliderect(cell_rect):
                pygame.draw.rect(screen, (40,40,50), cell_rect, border_radius=4)
                pygame.draw.rect(screen, (200,200,200), cell_rect, 1, border_radius=4)
                title = ALL_PERKS[perk.id]['title']
                text_surf = self.font.render(title, True, (220,220,220))
                screen.blit(text_surf, text_surf.get_rect(center=cell_rect.center))

            perk._rect = cell_rect  # сохраняем хитбокс для клика

    def handle_event(self, event: pygame.event.Event, character):
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.rect.collidepoint(event.pos):
                self.close()
                return

            for perk in self.perks:
                if perk._rect.collidepoint(event.pos):
                    if perk.id in [p.id for p in character.perks]:
                        continue
                    self.close()
                    return perk

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
