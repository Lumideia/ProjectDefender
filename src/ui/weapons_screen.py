import pygame

from src.enteties.weapon_instance import create_weapon_instance, MeleeWeaponInstance
from src.rules.dice import format_dice
from src.ui import runtime
from src.ui.fonts_colors import BLACK, LIGHT_GRAY, DARK_GRAY, GREEN
from src.constant.weapons import MAIN_WEAPONS, OTHER_WEAPONS
from src.rules.calc import LegacyCalculation
from src.rules.weapons.cover import Interference, Cover, Position


full_minus_rect = full_plus_rect = half_minus_rect = half_plus_rect = None

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = DARK_GRAY
        self.text = text
        self.txt_surface = runtime.fonts["main"].render(text, True, BLACK)
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return 'submit'
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
            self.txt_surface = runtime.fonts["main"].render(self.text, True, BLACK)
        return None
    def draw(self):
        pygame.draw.rect(runtime.screen, self.color, self.rect, 2)
        runtime.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

def draw_screen_weapons():
    # заголовки/подсказки
    draw_text("Оружейный помощник", 10, 40, color=BLACK)
    draw_category_tabs_weap()
    draw_weapon_buttons()
    draw_weapon_stats(get_current_weapons()[selected_weapon_index])
    compute_and_draw_effects()
    draw_environment_controls()


def handle_events_weapons(event):
    global selected_category, selected_weapon_index
    global full_interf_count, half_interf_count, selected_cover, selected_position

    result = weap_input_box.handle_event(event)
    if result == 'submit':
        pass
    if event.type == pygame.MOUSEBUTTONDOWN:
        # переключение вкладок оружия
        for cat, rect in tab_rects_weap.items():
            if rect.collidepoint(event.pos):
                selected_category = cat
                selected_weapon_index = 0
                weap_input_box.text = ""
                weap_input_box.txt_surface = runtime.fonts["main"].render("", True, BLACK)
        # выбор оружия
        for i, rect in button_rects_weap.items():
            if rect.collidepoint(event.pos):
                selected_weapon_index = i
                weap_input_box.text = ""
                weap_input_box.txt_surface = runtime.fonts["main"].render("", True, BLACK)
        # +/- помехи
        if full_minus_rect and full_minus_rect.collidepoint(event.pos):
            full_interf_count = max(0, full_interf_count - 1)
        if full_plus_rect and full_plus_rect.collidepoint(event.pos):
            full_interf_count += 1
        if half_minus_rect and half_minus_rect.collidepoint(event.pos):
            half_interf_count = max(0, half_interf_count - 1)
        if half_plus_rect and half_plus_rect.collidepoint(event.pos):
            half_interf_count += 1
        # радио-кнопки
        for key, rect in cover_radio_rects.items():
            if rect.collidepoint(event.pos):
                selected_cover = key
        for key, rect in pos_radio_rects.items():
            if rect.collidepoint(event.pos):
                selected_position = key


def draw_category_tabs_weap():
    global tab_rects_weap
    tab_rects_weap = {}
    tab_w, tab_h = 200, 36
    gap = 10
    x0, y0 = 10, 60
    tabs = [
        (CATEGORY_MAIN, "Основное оружие"),
        (CATEGORY_OTHER, "Другое оружие"),
    ]
    for i, (cat, title) in enumerate(tabs):
        x = x0 + i * (tab_w + gap)
        rect = pygame.Rect(x, y0, tab_w, tab_h)
        active = (selected_category == cat)
        pygame.draw.rect(runtime.screen, GREEN if active else LIGHT_GRAY, rect, 0)
        pygame.draw.rect(runtime.screen, BLACK, rect, 2)
        draw_text(title, rect.x + 10, rect.y + 9)
        tab_rects_weap[cat] = rect


def draw_weapon_buttons():
    global button_rects_weap
    button_rects_weap = {}
    weapons = get_current_weapons()
    for i, weapon in enumerate(weapons):
        width = 130
        height = 40
        x = 10 + i * width
        y = 110
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(runtime.screen, GREEN if i == selected_weapon_index else LIGHT_GRAY, rect)
        pygame.draw.rect(runtime.screen, BLACK, rect, 2)
        draw_text(weapon.name, x + 10, y + 10)
        button_rects_weap[i] = rect


def draw_weapon_stats(weapon):
    y = 180
    line_h = 30
    draw_text("Характеристики оружия:", 50, y); y += line_h
    base = getattr(weapon, 'base_dices', []) or []
    bonus = getattr(weapon, 'bonus_dices', []) or []
    dices = base + bonus
    draw_text(f"Урон: {format_dice(dices)}", 70, y); y += line_h
    draw_text(f"Крит: {format_dice(getattr(weapon, 'cr_dices', None))}", 70, y); y += line_h
    draw_text(f"Базовый урон (без кубов): {getattr(weapon, 'base_atk', 0)}", 70, y); y += line_h
    draw_text(f"Игнор брони: {getattr(weapon, 'armor_ignorance', 0)}", 70, y); y += line_h
    draw_text(f"Разрыв брони: {getattr(weapon, 'armor_destroying', 0)}", 70, y); y += line_h
    if hasattr(weapon, 'is_move_attack_allowed'):
        draw_text(f"Атака в движении: {'Да' if weapon.is_move_attack_allowed else 'Нет'}", 70, y); y += line_h

    for row in weapon.additional_info():
        draw_text(row, 70, y); y += line_h

    try:
        from src.rules.weapons.weapon import FirearmWeapon
        if isinstance(weapon, FirearmWeapon):
            draw_text(f"Магазин: {getattr(weapon, 'mag_size', '—')}", 70, y); y += line_h
            draw_text(f"Перезарядка: {getattr(weapon, 'reload_cost', '—')} AP", 70, y); y += line_h
            draw_text(f"Тяжёлое: {'Да' if getattr(weapon, 'is_heavy', False) else 'Нет'}", 70, y); y += line_h
    except Exception:
        pass


def draw_environment_controls():
    global full_minus_rect, full_plus_rect, half_minus_rect, half_plus_rect
    global cover_radio_rects, pos_radio_rects
    draw_text("Помехи на пути:", 550, 360)
    full_minus_rect, full_plus_rect = draw_count_selector(570, 395, "Полное:", full_interf_count)
    half_minus_rect, half_plus_rect = draw_count_selector(570, 435, "Половинчатое:", half_interf_count)
    cover_radio_rects = draw_radio_group(
        550, 480, "Укрытие:",
        [(COVER_FULL, "Full"), (COVER_HALF, "Half"), (COVER_NONE, "None")],
        selected_cover
    )
    pos_radio_rects = draw_radio_group(
        550, 530, "Позиция:",
        [(POS_HIGHER, "Выше"), (POS_EQUAL, "="), (POS_LOWER, "Ниже")],
        selected_position
    )


def compute_and_draw_effects():
    dist = 0
    weapon = get_current_weapons()[selected_weapon_index]

    interference = Interference(half=half_interf_count, full=full_interf_count)
    if selected_cover == COVER_FULL:
        cover_obj = Cover(is_full=True)
    elif selected_cover == COVER_HALF:
        cover_obj = Cover(is_full=False)
    else:
        cover_obj = Cover(is_full=None)
    if selected_position == POS_HIGHER:
        pos_enum = Position.HIGHER
    elif selected_position == POS_LOWER:
        pos_enum = Position.LOWER
    else:
        pos_enum = Position.EQUAL

    if not isinstance(weapon, MeleeWeaponInstance):
        draw_text("Введите дистанцию:", 550, 160)  # было 130
        weap_input_box.rect.y = 155  # было 125
        weap_input_box.draw()
        try:
            dist = int(weap_input_box.text)
        except (ValueError, TypeError):
            return

    try:
        calc = LegacyCalculation(
            weapon=weapon,
            distance=dist,
            relative_position=pos_enum,
            cover=cover_obj,
            interference=interference,
            character=selected_character,
        )
    except Exception:
        return

    base_accuracy = calc.base_acc + calc.distance_acc
    final_accuracy = calc.calculate_accuracy()
    acc_penalty = base_accuracy - final_accuracy
    cr = calc.calculate_cr()
    dmg_mult = calc.calculate_dmg_buff()
    draw_text("► Эффекты на этой дистанции:", 550, 190)
    draw_text(f"Базовая точность: {base_accuracy}%", 570, 210)
    draw_text(f"Штраф к точности: -{acc_penalty}%", 570, 230)
    draw_text(f"Итоговая точность: {final_accuracy}%", 570, 250)
    draw_text(f"Крит. шанс: {cr}%", 570, 270)
    draw_text(f"Множитель урона: ×{round(dmg_mult, 2)}", 570, 290)
    if selected_character and selected_character.crit_buff:
        draw_text(f"Множитель крит. урона: {selected_character.crit_buff}%", 570, 310)

def handle_event(event):
    handle_events_weapons(event)

def draw():
    draw_screen_weapons()


CATEGORY_MAIN = 'main'
CATEGORY_OTHER = 'other'
selected_category = CATEGORY_MAIN
custom_weapons: list = None
selected_weapon_index = 0
selected_character = None
weap_input_box = InputBox(780, 125, 80, 32)
full_interf_count = 0
half_interf_count = 0
COVER_FULL = "full"
COVER_HALF = "half"
COVER_NONE = "none"
selected_cover = COVER_NONE
POS_HIGHER = "higher"
POS_EQUAL = "equal"
POS_LOWER = "lower"
selected_position = POS_EQUAL


def get_current_weapons():
    # если передан список оружия персонажа – использовать его
    if custom_weapons is not None:
        return custom_weapons
    weapons = MAIN_WEAPONS if selected_category == CATEGORY_MAIN else OTHER_WEAPONS
    return [create_weapon_instance(weapon) for weapon in weapons]


def draw_text(text, x, y, *, color=BLACK, font=runtime.fonts["main"]):
    label = font.render(text, True, color)
    runtime.screen.blit(label, (x, y))


def draw_count_selector(x, y, label, count):
    draw_text(label, x, y)
    text_width = runtime.fonts["main"].size(label)[0]
    spacing = 20
    count_x = x + text_width + spacing
    minus_rect = pygame.Rect(count_x + 40, y - 5, 30, 30)
    plus_rect = pygame.Rect(count_x + 80, y - 5, 30, 30)
    pygame.draw.rect(runtime.screen, LIGHT_GRAY, minus_rect)
    pygame.draw.rect(runtime.screen, LIGHT_GRAY, plus_rect)
    pygame.draw.rect(runtime.screen, BLACK, minus_rect, 1)
    pygame.draw.rect(runtime.screen, BLACK, plus_rect, 1)
    draw_text("-", minus_rect.x + 10, minus_rect.y + 5)
    draw_text("+", plus_rect.x + 10, plus_rect.y + 5)
    draw_text(str(count), count_x, y)
    return minus_rect, plus_rect


def draw_radio_group(x, y, title, options, selected_key):
    draw_text(title, x, y)
    rects = {}
    bx, by = x, y + 26
    for key, label in options:
        rect = pygame.Rect(bx, by, 22, 22)
        pygame.draw.rect(runtime.screen, LIGHT_GRAY, rect)
        pygame.draw.rect(runtime.screen, BLACK, rect, 1)
        if key == selected_key:
            pygame.draw.circle(runtime.screen, BLACK, (rect.centerx, rect.centery), 6, 0)
        draw_text(label, rect.right + 8, rect.y + 2)
        rects[key] = rect
        bx += 120
    return rects


tab_rects_weap = {}
button_rects_weap = {}
cover_radio_rects = {}
pos_radio_rects = {}
