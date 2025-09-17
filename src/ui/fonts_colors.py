import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 180, 0)
BLUE = (40, 140, 240)

def get_fonts():
    return {
        "main":  pygame.font.SysFont("arial", 17),
        "small": pygame.font.SysFont("consolas", 14)
    }
