import pygame as pg

from project.constants import Color, SliderProperties


class VolumeIndicator:
    """Volume indicator to show the volume."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 100)
        self.volume = int()

    def draw(self) -> None:
        """Draws and renders the volume."""
        indicator = self.font.render(str(int(self.volume)), True, Color.orange)
        self.screen.blit(indicator, (1050, SliderProperties.body_y - 30))
