from __future__ import annotations

from typing import Optional, List, Union

import pygame

from src.enteties.character_instance import CharacterInstance
from src.enteties.weapon_instance import FireArmWeaponInstance, MeleeWeaponInstance, ThrowingWeaponInstance
from src.ui.theme import COLORS



class ToggleButton:
    def __init__(self, label: str, get_state: callable, set_state: callable):
        self.label = label
        self.get_state = get_state     # функция возвращает True/False
        self.set_state = set_state     # функция принимает новое значение
        self.rect: Optional[pygame.Rect] = None

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, x: int, y: int, size: int):
        self.rect = pygame.Rect(x, y, size, size)
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)

        # цвет зависит от состояния
        active = self.get_state()
        base_col = (40,120,40) if active else (60,60,60)
        pygame.draw.rect(screen, base_col if not hovered else (80,80,80), self.rect, border_radius=6)
        pygame.draw.rect(screen, COLORS['FRAME'], self.rect, 1, border_radius=6)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                self.set_state(not self.get_state())


class StatButton:
    def __init__(self, text: str, action: callable):
        self.text = text
        self.action = action
        self.rect: Optional[pygame.Rect] = None  # позицию выставляем при рендере

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, x: int, y: int, size: int):
        self.rect = pygame.Rect(x, y, size, size)
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)
        pygame.draw.rect(screen, COLORS['BTN_HL'] if hovered else COLORS['BTN'], self.rect, border_radius=6)
        pygame.draw.rect(screen, COLORS['FRAME'], self.rect, 1, border_radius=6)
        label = font.render(self.text, True, COLORS['TEXT'])
        screen.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                self.action()


class StatControl:
    def __init__(self, title: str, value_getter: callable, buttons: List[Union[StatButton, ToggleButton]]):
        self.title = title
        self.value_getter = value_getter
        self.buttons = buttons

    def draw(self, screen: pygame.Surface, font: pygame.font.Font,
             x: int, y: int, width: int, btn_size: int):
        # текст и значение
        val = self.value_getter()
        text = font.render(f"{self.title}: {val}", True, COLORS['TEXT'])
        screen.blit(text, (x + 10, y))

        # кнопки справа
        bx = x + width - btn_size - 10
        for btn in self.buttons:
            btn.draw(screen, font, bx, y, btn_size)
            bx -= btn_size + 6  # шаг влево для следующей кнопки

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)


class CharacterStatsPanel:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont("arial", 18)
        self.btn_size = 24
        self.character: Optional[CharacterInstance] = None
        self.controls: List[StatControl] = []

    def set_character(self, character: CharacterInstance):
        self.character = character
        self.controls = []
        # HP: только +/-
        self.controls.append(
            StatControl(
                "Уклонение",
                lambda: self.character.dodge,
                [
                    StatButton("-", lambda: setattr(self.character, "dodge", max(0, self.character.dodge - 1))),
                    StatButton("+", lambda: setattr(self.character, "dodge", self.character.dodge + 1)),
                ]
            )
        )
        # Armour: только +/-
        self.controls.append(
            StatControl(
                "Мобильность",
                lambda: self.character.mobility,
                [
                    StatButton("-", lambda: setattr(self.character, "mobility", max(0, self.character.mobility - 1))),
                    StatButton("+", lambda: setattr(self.character, "mobility", self.character.mobility + 1)),
                ]
            )
        )
        self.controls.append(
            StatControl(
                "Меткость",
                lambda: self.character.accuracy,
                [
                    StatButton("-", lambda: setattr(self.character, "accuracy", max(0, self.character.accuracy - 1))),
                    StatButton("+", lambda: setattr(self.character, "accuracy", self.character.accuracy + 1)),
                ]
            )
        )
        # Bullets: +/– и Reload
        if isinstance(self.character.main_weapon, FireArmWeaponInstance):
            wpn = self.character.main_weapon
            self.controls.append(
                StatControl(
                    "Пули",
                    lambda: wpn.current_ammo,
                    [
                        StatButton("-", wpn.shoot),  # например уменьшить на 1
                        StatButton("+", wpn.load_bullets),
                        StatButton("R", wpn.reload),  # перезарядка
                    ]
                )
            )
        if self.character.side_weapon is not None:
            if isinstance(self.character.side_weapon, FireArmWeaponInstance):
                side_wpn = self.character.side_weapon
                self.controls.append(
                    StatControl(
                        "Пули зап.",
                        lambda: side_wpn.current_ammo,
                        [
                            StatButton("-", side_wpn.shoot),  # например уменьшить на 1
                            StatButton("+", side_wpn.load_bullets),
                            StatButton("R", side_wpn.reload),  # перезарядка
                        ]
                    )
                )
            elif isinstance(self.character.side_weapon, ThrowingWeaponInstance):
                wpn = self.character.side_weapon
                self.controls.append(
                    StatControl(
                        "Кол-во",
                        lambda: wpn.count,
                        [
                            StatButton("-", wpn.throw),  # например уменьшить на 1
                            StatButton("+", wpn.pick_up),
                        ]
                    )
                )


        self.controls.append(
            StatControl(
                "Наблюдение",
                lambda: "",
                [
                    ToggleButton(
                        "Watch",
                        lambda: self.character.observation,
                        lambda val: setattr(self.character, "observation", val)
                    )
                 ]
            )
        )

    def draw(self, screen: pygame.Surface):
        if not self.character:
            return
        pygame.draw.rect(screen, (18,18,28), self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['FRAME'], self.rect, 1, border_radius=8)
        y = self.rect.y + 10
        for ctrl in self.controls:
            ctrl.draw(screen, self.font, self.rect.x, y, self.rect.width, self.btn_size)
            y += 40  # смещение между строками

    def handle_event(self, event: pygame.event.Event):
        if not self.character:
            return
        for ctrl in self.controls:
            ctrl.handle_event(event)
