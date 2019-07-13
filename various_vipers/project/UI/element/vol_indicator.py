from pygame import Surface
from pygame.font import Font

from project.constants import Color, SliderProperties


class VolumeIndicator:
    """Volume indicator to show the volume."""

    def __init__(self, screen: Surface, number: float):
        self.screen = screen
        self.number = number

        self.font = Font(None, 100)
        self.volume = int()

    def draw(self) -> None:
        """Draws and renders the volume."""
        top = SliderProperties.body_y - 30
        if self.number == 2:
            top = SliderProperties.body_y + 100

        indicator = self.font.render(str(int(self.volume)), True, Color.orange)
        self.screen.blit(
            indicator, (SliderProperties.body_x + SliderProperties.body_width + 20, top)
        )
