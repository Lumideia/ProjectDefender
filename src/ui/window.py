from typing import Tuple

import pygame

# default ---
DEFAULT_WIDTH  = 1280
DEFAULT_HEIGHT = 720
DEFAULT_TITLE  = "Тактический помощник"


def create_window(
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    title: str = DEFAULT_TITLE
) -> Tuple[pygame.Surface, pygame.time.Clock]:
    """Создаёт окно pygame и возвращает (screen, clock)."""
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return screen, clock
