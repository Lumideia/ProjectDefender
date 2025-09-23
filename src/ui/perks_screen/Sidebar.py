from typing import List, Tuple, Callable

import pygame

from src.enteties.character_instance import CharacterInstance, Grenadier
from src.ui.theme import COLORS


class Sidebar:
    """Боковая панель выбора персонажей со скроллом и кнопками"""

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 visible_rows: int = 4,
                 item_height: int = 44):
        self.x, self.y = x, y
        self.width = width
        self.visible_rows = visible_rows
        self.item_height = item_height
        self.margin = 10

        # список персонажей
        self.characters: List[Tuple["CharacterInstance", str]] = []
        self.active_idx: int = -1

        # колбэки (назначаются снаружи)
        self.on_select:   Callable[[int], None] = lambda idx: None
        self.on_add:      Callable[[], None]    = lambda: None
        self.on_delete:   Callable[[], None]    = lambda: None
        self.on_rename:   Callable[[int], None] = lambda idx: None

        # скролл (номер первой видимой записи)
        self.scroll = 0

        # кнопки
        self.btn_add    = pygame.Rect(self.x + self.width - 150, self.y - 40, 40, 40)
        self.btn_rename = pygame.Rect(self.x + self.width - 100, self.y - 40, 40, 40)
        self.btn_del    = pygame.Rect(self.x + self.width -  50, self.y - 40, 40, 40)

        # цвета и шрифты (используйте ваши константы)
        self.COLOR_BG    = (18, 18, 28)
        self.COLOR_ITEM  = (50, 50, 60)
        self.COLOR_ITEM_ACTIVE = (40, 80, 140)
        self.COLOR_BTN   = (60, 60, 60)
        self.COLOR_BTN_HL= (90, 90, 90)
        self.font_small  = pygame.font.SysFont("arial", 16)
        self.font_title  = pygame.font.SysFont("arial", 28, bold=True)

    # ---------- работа со списком ----------
    def add_character(self, char: Grenadier, name: str):
        self.characters.append((char, name))
        self.active_idx = len(self.characters) - 1
        self._scroll_to_active()

    def set_active(self, idx: int):
        self.active_idx = max(0, min(idx, len(self.characters) - 1))
        self._scroll_to_active()

    def _scroll_to_active(self):
        """Держим активного в видимой зоне"""
        if self.active_idx < self.scroll:
            self.scroll = self.active_idx
        elif self.active_idx >= self.scroll + self.visible_rows:
            self.scroll = self.active_idx - self.visible_rows + 1

    # ---------- отрисовка ----------
    def draw(self, screen: pygame.Surface):
        area = pygame.Rect(self.x, self.y, self.width, self.visible_rows * (self.item_height + self.margin) + 2*self.margin)
        pygame.draw.rect(screen, self.COLOR_BG, area, border_radius=8)

        # кнопки
        self._draw_button(screen, self.btn_add, "+")
        self._draw_button(screen, self.btn_rename, "✏")
        self._draw_button(screen, self.btn_del, "🗑")

        # видимые персонажи
        y_off = self.y + self.margin
        for i in range(self.scroll, min(len(self.characters), self.scroll + self.visible_rows)):
            _, name = self.characters[i]
            rect = pygame.Rect(self.x + self.margin, y_off,
                               self.width - 2 * self.margin, self.item_height)
            active = (i == self.active_idx)
            pygame.draw.rect(screen,
                             self.COLOR_ITEM_ACTIVE if active else self.COLOR_ITEM,
                             rect, border_radius=6)
            pygame.draw.rect(screen,COLORS['FRAME'], rect, 1, border_radius=6)
            label = self.font_small.render(name, True, COLORS['TEXT'])
            screen.blit(label, (rect.x + 10, rect.y + 10))
            # сохраним для хит-теста
            setattr(self, f"_rect_{i}", rect)
            y_off += self.item_height + self.margin

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, text: str):
        mx, my = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mx, my)
        pygame.draw.rect(screen, self.COLOR_BTN_HL if hovered else self.COLOR_BTN, rect, border_radius=6)
        pygame.draw.rect(screen, COLORS['FRAME'], rect, 1, border_radius=6)
        label = self.font_title.render(text, True, COLORS['TEXT'])
        screen.blit(label, label.get_rect(center=rect.center))

    # ---------- обработка событий ----------
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_add.collidepoint(event.pos):
                self.on_add()
                return
            if self.btn_rename.collidepoint(event.pos):
                self.on_rename(self.active_idx)
                return
            if self.btn_del.collidepoint(event.pos):
                self.on_delete()
                return

            # выбор персонажа
            for i in range(len(self.characters)):
                r = getattr(self, f"_rect_{i}", None)
                if r and r.collidepoint(event.pos):
                    self.set_active(i)
                    self.on_select(i)
                    return

        # прокрутка колесом
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0 and self.scroll > 0:
                self.scroll -= 1
            elif event.y < 0 and self.scroll + self.visible_rows < len(self.characters):
                self.scroll += 1
