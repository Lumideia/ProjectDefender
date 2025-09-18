from enum import IntEnum, auto

import pygame

from src.ui import runtime
from src.ui.window import DEFAULT_WIDTH, DEFAULT_HEIGHT
from src.ui.fonts_colors import BLACK
from src.ui.weapons_screen import draw_text


screen = runtime.screen
FONT = runtime.fonts["main"]
FONT_SMALL = runtime.fonts["small"]

GRID_W, GRID_H = 34, 18
SCREEN_W, SCREEN_H = DEFAULT_WIDTH, DEFAULT_HEIGHT


def handle_events_map(event):
    global show_fov, fov_radius
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_w, pygame.K_UP):    try_move(0, -1)
        elif event.key in (pygame.K_s, pygame.K_DOWN): try_move(0, 1)
        elif event.key in (pygame.K_a, pygame.K_LEFT): try_move(-1, 0)
        elif event.key in (pygame.K_d, pygame.K_RIGHT):try_move(1, 0)
        elif event.key == pygame.K_r: show_fov = not show_fov
        elif event.key == pygame.K_LEFTBRACKET:  fov_radius = max(2, fov_radius - 1)
        elif event.key == pygame.K_RIGHTBRACKET: fov_radius = min(30, fov_radius + 1)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = grid_from_mouse(event.pos)
        if not in_bounds(x, y): return
        if event.button == 1:
            cycle_tile(x, y)
        elif event.button == 3:
            if has_door(x, y):
                remove_door(x, y)
            else:
                toggle_door(x, y)
        elif event.button == 4:
            if has_door(x, y): doors[(x, y)] = True
        elif event.button == 5:
            if has_door(x, y): doors[(x, y)] = False


def draw_screen_map():
    # заголовок
    draw_text("Карта / ЛОС / Двери", 10, 40, color=BLACK)
    draw_grid_map()

def handle_event(event):
    handle_events_map(event)

def draw():
    draw_screen_map()


TILE = 24


class Tile(IntEnum):
    EMPTY = 0
    OBSTACLE = auto()  # блок ЛОС
    WALL = auto()      # блок ход+ЛОС


grid = [[Tile.EMPTY for _ in range(GRID_H)] for _ in range(GRID_W)]
doors = {}  # (x,y) -> bool open?
player_pos = [GRID_W // 2, GRID_H // 2]
fov_radius = 10
show_fov = True


def in_bounds(x, y): return 0 <= x < GRID_W and 0 <= y < GRID_H


def door_open(x, y): return doors.get((x, y), None) is True


def has_door(x, y):  return (x, y) in doors


def toggle_door(x, y):
    if (x, y) in doors: doors[(x, y)] = not doors[(x, y)]
    else: doors[(x, y)] = False


def remove_door(x, y):
    if (x, y) in doors: del doors[(x, y)]


def tile_blocks_move(x, y):
    if not in_bounds(x, y): return True
    if grid[x][y] == Tile.WALL: return True
    if (x, y) in doors and not door_open(x, y): return True
    return False


def tile_blocks_los(x, y):
    if not in_bounds(x, y): return True
    if grid[x][y] in (Tile.OBSTACLE, Tile.WALL): return True
    if (x, y) in doors and not door_open(x, y): return True
    return False


def los_clear(x0, y0, x1, y1):
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    err = dx - dy
    while not (x == x1 and y == y1):
        e2 = 2 * err
        if e2 > -dy: err -= dy; x += sx
        if e2 < dx:  err += dx; y += sy
        if (x, y) != (x1, y1) and tile_blocks_los(x, y):
            return False
    return True


def calc_fov(cx, cy, radius):
    visible = set()
    r2 = radius * radius
    for x in range(max(0, cx - radius), min(GRID_W, cx + radius + 1)):
        for y in range(max(0, cy - radius), min(GRID_H, cy + radius + 1)):
            if (x - cx)*(x - cx) + (y - cy)*(y - cy) <= r2:
                if los_clear(cx, cy, x, y):
                    visible.add((x, y))
    return visible


def draw_grid_map():
    # поле
    for x in range(GRID_W):
        for y in range(GRID_H):
            rect = pygame.Rect(x * TILE, y * TILE + 48, TILE, TILE)
            t = grid[x][y]
            color = (58, 66, 78) if t == Tile.EMPTY else ((120, 120, 35) if t == Tile.OBSTACLE else (80, 30, 30))
            pygame.draw.rect(screen, color, rect)
    # двери
    for (x, y), opened in doors.items():
        rect = pygame.Rect(x * TILE + 4, y * TILE + 4 + 48, TILE - 8, TILE - 8)
        pygame.draw.rect(screen, (200, 170, 100) if opened else (160, 110, 40), rect, border_radius=4)
    # игрок
    pygame.draw.rect(
        screen, (100, 200, 255),
        pygame.Rect(player_pos[0]*TILE + 4, player_pos[1]*TILE + 4 + 48, TILE - 8, TILE - 8),
        border_radius=4
    )
    # FOV
    if show_fov:
        visible = calc_fov(player_pos[0], player_pos[1], fov_radius)
        shade = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 180))
        for (x, y) in visible:
            pygame.draw.rect(shade, (0, 0, 0, 0), (x*TILE, y*TILE + 48, TILE, TILE))
        screen.blit(shade, (0, 0))
    # сетка
    for x in range(GRID_W + 1):
        pygame.draw.line(screen, (40, 40, 48), (x*TILE, 48), (x*TILE, 48 + GRID_H*TILE))
    for y in range(GRID_H + 1):
        pygame.draw.line(screen, (40, 40, 48), (0, 48 + y*TILE), (GRID_W*TILE, 48 + y*TILE))
    # подсказки
    draw_text("Редактор карты: LMB цикл тайла, RMB дверь, колесо — открыть/закрыть",
              10, 48 + GRID_H * TILE + 6, font=FONT_SMALL)

    draw_text("WASD/стрелки — ходить, R — FOV, [ / ] — радиус",
              10, 48 + GRID_H * TILE + 24, font=FONT_SMALL)


def grid_from_mouse(pos):
    mx, my = pos
    gx = mx // TILE
    gy = (my - 48) // TILE
    return gx, gy


def cycle_tile(x, y):
    t = grid[x][y]
    if t == Tile.EMPTY: grid[x][y] = Tile.OBSTACLE
    elif t == Tile.OBSTACLE: grid[x][y] = Tile.WALL
    else: grid[x][y] = Tile.EMPTY


def try_move(dx, dy):
    nx, ny = player_pos[0] + dx, player_pos[1] + dy
    if in_bounds(nx, ny) and not tile_blocks_move(nx, ny):
        player_pos[0], player_pos[1] = nx, ny
