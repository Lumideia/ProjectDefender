import pygame

from src.enteties.character_instance import CHARACTER_CLASSES
from src.enteties.weapon_instance import create_weapon_instance


class CreateCharacterForm:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.active = False

        # состояние выбора
        self.selected_class = 0
        self.selected_weapon = 0
        self.selected_side_weapon = 0
        self.available_weapons = CHARACTER_CLASSES[self.selected_class].available_weapons
        self.available_side_weapons = CHARACTER_CLASSES[self.selected_class].available_side_weapons
        self.name_text = ""

        self.font = pygame.font.SysFont("arial", 20)
        self.rect = pygame.Rect(400, 40, 600, 600)

        self.btn_create = pygame.Rect(self.rect.x + 100, self.rect.bottom - 60, 200, 40)
        self.btn_cancel = pygame.Rect(self.rect.x + 320, self.rect.y + 10, 60, 30)

    def open(self):
        self.active = True
        self.name_text = ""

    def close(self):
        self.active = False

    def draw(self):
        if not self.active:
            return
        pygame.draw.rect(self.screen, (30,30,40), self.rect, border_radius=8)
        pygame.draw.rect(self.screen, (180,180,180), self.rect, 2, border_radius=8)

        # --- заголовок
        title = self.font.render("Create character", True, (220,220,220))
        self.screen.blit(title, (self.rect.x + 20, self.rect.y + 20))

        # --- выбор класса
        self.screen.blit(self.font.render("Class:", True, (220,220,220)),
                         (self.rect.x + 20, self.rect.y + 60))
        for i, cls in enumerate(CHARACTER_CLASSES):
            txt = f"[{'x' if i==self.selected_class else ' '}] {cls.class_name}"
            self.screen.blit(self.font.render(txt, True, (220,220,220)),
                             (self.rect.x + 40, self.rect.y + 90 + i*25))

        # --- выбор оружия
        self.screen.blit(self.font.render("Weapon:", True, (220,220,220)),
                         (self.rect.x + 280, self.rect.y + 60))

        for j, w in enumerate(self.available_weapons):
            txt = f"[{'x' if j==self.selected_weapon else ' '}] {w.name}"
            self.screen.blit(self.font.render(txt, True, (220,220,220)),
                             (self.rect.x + 300,
                              self.rect.y + 90 + j*25))

        self.screen.blit(self.font.render("Side weapon:", True, (220,220,220)),
                         (self.rect.x + 280, self.rect.y + 220))

        if self.available_side_weapons:
            for j, w in enumerate(self.available_side_weapons):
                txt = f"[{'x' if j==self.selected_side_weapon else ' '}] {w.name if w is not None else 'Ничего'}"
                self.screen.blit(self.font.render(txt, True, (220, 220, 220)),
                                 (self.rect.x + 300,
                                  self.rect.y + 250 + j * 25))


        # --- ввод имени
        y_name = self.rect.y + 160 + len(CHARACTER_CLASSES)*25
        self.screen.blit(self.font.render("Name:", True, (220,220,220)), (self.rect.x + 20, y_name))
        pygame.draw.rect(self.screen, (50,50,60),
                         (self.rect.x + 100, y_name - 5, 200, 30), border_radius=4)
        txtsurf = self.font.render(self.name_text, True, (220,220,220))
        self.screen.blit(txtsurf, (self.rect.x + 110, y_name))

        # --- кнопки
        self._draw_button(self.btn_create, "Create")
        self._draw_button(self.btn_cancel, "X")

    def _draw_button(self, rect, text):
        mx, my = pygame.mouse.get_pos()
        col = (90,90,90) if rect.collidepoint(mx,my) else (60,60,60)
        pygame.draw.rect(self.screen, col, rect, border_radius=6)
        pygame.draw.rect(self.screen, (180,180,180), rect, 1, border_radius=6)
        label = self.font.render(text, True, (220,220,220))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self._create_character()
            elif event.key == pygame.K_ESCAPE:
                self.close()
            elif event.key == pygame.K_BACKSPACE:
                self.name_text = self.name_text[:-1]
            else:
                if event.unicode.isprintable():
                    self.name_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # выбор класса
            for i in range(len(CHARACTER_CLASSES)):
                line_y = self.rect.y + 90 + i*25
                if pygame.Rect(self.rect.x + 40, line_y, 250, 25).collidepoint(event.pos):
                    self.selected_class = i
                    self.selected_weapon = 0
                    self.selected_side_weapon = 0

            # выбор оружия
            self.available_weapons = CHARACTER_CLASSES[self.selected_class].available_weapons
            for i in range(len(self.available_weapons)):
                line_y1 = self.rect.y + 90 + i*25
                if pygame.Rect(self.rect.x + 300, line_y1, 400, 25).collidepoint(event.pos):
                    self.selected_weapon = i

            self.available_side_weapons = CHARACTER_CLASSES[self.selected_class].available_side_weapons
            for j in range(len(self.available_side_weapons)):
                line_y2 = self.rect.y + 250 + j * 25
                if pygame.Rect(self.rect.x + 300, line_y2, 400, 50).collidepoint(event.pos):
                    self.selected_side_weapon = j



            # кнопки
            if self.btn_create.collidepoint(event.pos):
                return self._create_character()
            if self.btn_cancel.collidepoint(event.pos):
                self.close()
        return None

    def _create_character(self):
        cls = CHARACTER_CLASSES[self.selected_class]
        weapon = self.available_weapons[self.selected_weapon]

        side_weapon = self.available_side_weapons[self.selected_side_weapon] if self.selected_side_weapon is not None else None
        name = self.name_text or f"{cls.class_name} #{pygame.time.get_ticks()}"
        char = cls()
        char.main_weapon = create_weapon_instance(weapon)
        char.side_weapon = create_weapon_instance(side_weapon) if side_weapon else None
        if char.side_weapon:
            print(char.main_weapon.weapon.name, char.side_weapon.weapon.name)
        else:
            print('No')
        char.character.name = name
        self.close()
        return char
