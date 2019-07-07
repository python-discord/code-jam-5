import time
from typing import Optional

from pygame import Surface
from pygame.font import Font

from project.constants import Color, HEIGHT, WIDTH
from project.utils.helpers import fit_to_range


class Notification:
    """Notification to be displayed on screen."""

    def __init__(self, text: str, color: Color, duration: float = 2):
        self.text = text
        self.color = color
        self.duration = duration

        # Start time when notification showed up
        self.start = time.time()

    def draw(self, screen: Surface) -> Optional["Notification"]:
        """Draw notification on screen. Returns self if it still has drawing to do."""
        alpha = fit_to_range(
            min(time.time() - self.start, self.duration), 0, self.duration, 400, 0
        )

        font = Font(None, 50)
        text_surface = font.render(self.text, True, self.color)

        # Top middle of the screen
        w = int(WIDTH // 2) - int(text_surface.get_width() // 2)
        h = int(HEIGHT // 6)
        screen.blit(text_surface, (w, h))

        # We use alpha to check if notification should be still drawn
        return self if alpha > 0 else None
