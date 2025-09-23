import pygame
import sys


from src.ui import runtime
from src.ui.fonts_colors import WHITE, BLACK, LIGHT_GRAY, BLUE, get_fonts

pygame.init()

runtime.screen = pygame.display.set_mode((1280, 720))
runtime.clock  = pygame.time.Clock()
runtime.fonts  = get_fonts()

from src.ui import map_screen, weapons_screen
from src.ui.perks_screen.perk_screen import PerkScreen



screen = runtime.screen
runtime.current_screen = weapons_screen
FONT = runtime.fonts["main"]
FONT_SMALL = runtime.fonts["small"]
perk_screen = PerkScreen(screen)

SCREEN_MAP = {
    "weapons": weapons_screen,
    "map":     map_screen,
    "perks":   perk_screen
}

mode = SCREEN_MAP['weapons']


def draw_top_tabs():
    global TAB_RECTS
    TAB_RECTS = {}
    tabs = [
        ("weapons", "Оружие  (F1)"),
        ("map", "Карта   (F2)"),
        ("perks", "Персонаж (F3)")
    ]
    x, y, w, h, gap = 10, 8, 160, 30, 12
    for name, title in tabs:
        rect = pygame.Rect(x, y, w, h)
        active = (mode == name)
        pygame.draw.rect(screen, BLUE if active else LIGHT_GRAY, rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
        label = FONT.render(title, True, BLACK if not active else WHITE)
        screen.blit(label, (rect.x + 12, rect.y + 6))
        TAB_RECTS[name] = rect
        x += w + gap


TAB_RECTS = {
    SCREEN_MAP['weapons']: pygame.Rect(20, 20, 120, 40),
    SCREEN_MAP['map']:     pygame.Rect(160, 20, 120, 40),
    SCREEN_MAP['perks']:   pygame.Rect(300, 20, 120, 40)
}

while True:
    screen.fill(WHITE)
    draw_top_tabs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # проброс событий активному экрану
        if runtime.current_screen:
            runtime.current_screen.handle_event(event)

        # переключение по горячим клавишам
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                runtime.current_screen = weapons_screen
                weapons_screen.custom_weapons = None
            elif event.key == pygame.K_F2:
                runtime.current_screen = map_screen
            elif event.key == pygame.K_F3:
                runtime.current_screen = perk_screen

        # клик по вкладкам
        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in TAB_RECTS.items():
                if rect.collidepoint(event.pos):
                    runtime.current_screen = SCREEN_MAP[name]
    # ---- отрисовка ----
    if runtime.current_screen:
        runtime.current_screen.draw()

    pygame.display.flip()
    runtime.clock.tick(60)
