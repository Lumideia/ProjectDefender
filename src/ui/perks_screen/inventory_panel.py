import pygame
from typing import Optional, Callable, List

from src.enteties.character_instance import CharacterInstance
from src.rules.consumables.Inventory import Inventory
from src.ui.theme import COLORS
from src.rules.consumables.consumable import DEFAULT_CONSUMABLES  # список всех доступных

class InventoryPanel:
    def __init__(self, x:int, y:int, w:int, *, cells_x:int = 2, cells_y:int = 6, gap:int = 12):
        """
        w – общая ширина панели,
        cells_x / cells_y – количество ячеек по горизонтали/вертикали,
        gap – отступ между ячейками
        """
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.cell = (w - 50 - gap*(cells_x-1)) // cells_x
        self.gap = gap
        h = self.cell * cells_y + gap*(cells_y-1)
        self.rect = pygame.Rect(x, y, w, h)

        self.hovered: Optional[str] = None
        self.hovered_desc: Optional[str] = None

        self.modal_hovered: Optional[str] = None
        self.modal_hovered_desc: Optional[str] = None

        self.add_btn = pygame.Rect(self.rect.left + 20, self.rect.bottom + 20, 120, 50)
        self.modal_open = False
        self.modal_rect = pygame.Rect(self.rect.centerx-75, self.rect.centery-50, 300, 250)
        self.character = None
        self.mini_font = pygame.font.SysFont("arial", 14)

    def set_character(self, character: CharacterInstance):
        self.character = character
        # если нужно: создать сам Inventory, если его ещё нет
        if not hasattr(character, "inventory"):
            character.inventory = Inventory(space=16)

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Переносит текст по словам чтобы не выходил за max_width."""
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, inventory: Inventory):
        # фон панели
        pygame.draw.rect(screen, (18, 18, 28), self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['FRAME'], self.rect, 1, border_radius=8)

        # кнопка добавления
        pygame.draw.rect(screen, COLORS['BTN_HL'], self.add_btn, border_radius=6)
        screen.blit(font.render("Добавить", True, COLORS['TEXT']),
                    self.add_btn.move(10, 10))

        grid_width = self.cells_x * self.cell + (self.cells_x - 1) * self.gap
        grid_height = self.cells_y * self.cell + (self.cells_y - 1) * self.gap
        offset_x = self.rect.x + (self.rect.width - grid_width) // 2
        offset_y = self.rect.y + (self.rect.height - grid_height) // 2

        self.hovered = None
        self.hovered_desc = None
        items = list(inventory.consumables.items())
        idx = 0
        for row in range(self.cells_y):
            for col in range(self.cells_x):
                # координаты ячейки
                cx = offset_x + col * (self.cell + self.gap)
                cy = offset_y + row * (self.cell + self.gap)
                rect = pygame.Rect(cx, cy, self.cell, self.cell)

                # определяем цвет: активная или неактивная
                cell_index = row * self.cells_x + col
                is_active = cell_index < self.character.inventory.space
                base_color = (60, 60, 60) if is_active else (20, 20, 20)

                pygame.draw.rect(screen, base_color, rect, border_radius=6)
                pygame.draw.rect(screen, COLORS['FRAME'], rect, 1, border_radius=6)

                if idx < len(items):
                    name, count = items[idx]
                    text = f"{name} x{count}"
                    lines = self._wrap_text(text, self.mini_font, self.cell - 8)
                    text_height = len(lines) * self.mini_font.get_height()
                    start_y = rect.y + (rect.height - text_height) // 2
                    for line in lines:
                        surf = self.mini_font.render(line, True, COLORS['TEXT'])
                        screen.blit(surf, surf.get_rect(centerx=rect.centerx, y=start_y))
                        start_y += self.mini_font.get_height()
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        self.hovered = name
                        self.hovered_desc = next(
                            (c.description for c in DEFAULT_CONSUMABLES if c.class_name == name),
                            ""
                        )
                idx += 1

        if self.modal_open:
            self.draw_modal(screen, font, inventory)

    def draw_modal(self, screen: pygame.Surface, font: pygame.font.Font, inventory: Inventory):
        shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 160))
        screen.blit(shade, (0, 0))
        pygame.draw.rect(screen, (30, 30, 40), self.modal_rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['FRAME'], self.modal_rect, 1, border_radius=8)

        y = self.modal_rect.y + 10
        for c in DEFAULT_CONSUMABLES:
            line_rect = pygame.Rect(self.modal_rect.x + 10, y, 280, 30)
            txt = font.render(c.class_name, True, COLORS['TEXT'])
            screen.blit(txt, (self.modal_rect.x + 10, y))
            # --- проверка наведения ---
            if line_rect.collidepoint(pygame.mouse.get_pos()):
                self.modal_hovered = c.class_name
                self.modal_hovered_desc = c.description
            y += 30

    def handle_modal_event(self, event: pygame.event.Event, inventory: Inventory):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.modal_rect.collidepoint(event.pos):
                y = self.modal_rect.y + 10
                for c in DEFAULT_CONSUMABLES:
                    line_rect = pygame.Rect(self.modal_rect.x + 10, y, 280, 30)
                    if line_rect.collidepoint(event.pos):
                        inventory.add_consumable(c.class_name)
                        return True  # сигнал: закрыть модалку
                    y += 30
        return False

    def handle_event(self, event: pygame.event.Event, inventory: Inventory, on_add: Callable):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.add_btn.collidepoint(event.pos):
                on_add()  # <<< вызываем колбэк из PerkScreen
                return
            elif self.modal_open and self.modal_rect.collidepoint(event.pos):
                # клик по варианту в модалке
                y = self.modal_rect.y + 10
                for c in DEFAULT_CONSUMABLES:
                    line_rect = pygame.Rect(self.modal_rect.x + 10, y, 280, 30)
                    if line_rect.collidepoint(event.pos):
                        inventory.add_consumable(c.class_name)
                        self.modal_open = False
                        break
                    y += 30
            else:
                # использование предмета
                if self.hovered:
                    inventory.use_consumable(self.hovered)
