import time
from typing import Optional

import pygame as pg

from project.constants import Color, HEIGHT, WIDTH
from project.utils.helpers import fit_to_range


class Notification:
    """Notification to be displayed on screen."""

    def __init__(self, text: str, color: Color, duration: float = 2):
        self.text = text
        self.color = color
        self.duration = duration

        self.start = time.time()

    def draw(self, screen: pg.Surface) -> Optional["Notification"]:
        """Draw notification on screen. Returns self if it still has drawign to do."""
        alpha = fit_to_range(
            min(time.time() - self.start, self.duration), 0, self.duration, 400, 0
        )

        font = pg.font.Font(None, 50)
        text_surface = font.render(self.text, False, self.color)
        text_surface.set_alpha(alpha)

        w = int(WIDTH // 2) - int(text_surface.get_width() // 2)
        h = int(HEIGHT // 6)
        screen.blit(text_surface, (w, h))

        return self if alpha > 0 else None
