import pygame


class DoubleClickTracker:
    def __init__(self, delay_ms=200):
        self.delay_ms = delay_ms
        self._last_time = 0
        self._armed = False

    def is_double_click(self):
        now = pygame.time.get_ticks()
        diff = now - self._last_time
        self._last_time = now
        if self._armed and diff < self.delay_ms:
            self._armed = False
            return True
        self._armed = True
        return False
