"""Game model."""
import pygame as pg

from project.UI.main_menu import MainMenu
from project.constants import Color, FPS, HEIGHT, WIDTH


class Game:
    """Represents main game class."""

    def __init__(self):
        """Set initial values."""
        pg.init()
        pg.display.set_caption("Various Vipers game in development")

        self.running = True

        self.mouse_x = self.mouse_y = int()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.main_menu = MainMenu(self.screen)

    def run(self):
        """Draw and get events."""
        self.clock.tick(FPS)
        self._get_events()
        self._draw()

    def _get_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        print(self.mouse_x, self.mouse_y)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        self.screen.fill(Color.black)
        self.main_menu.draw()

        pg.display.flip()
