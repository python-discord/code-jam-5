"""Game model."""
import pygame as pg

from project.UI.main_menu import MainMenu
from project.UI.options import Options
from project.constants import Color, FPS, HEIGHT, WIDTH
from project.gameplay.game_view import GameView


class Game:
    """Represents main game class."""

    def __init__(self, start_game=False):
        """Set initial values."""
        pg.init()
        pg.display.set_caption("Various Vipers game in development")

        self.running = True
        self.playing = start_game

        self.mouse_x = self.mouse_y = int()
        self.event = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.page_state = None

        self.main_menu = MainMenu(self.screen)
        self.options = Options(self.screen)
        # Start new game
        self.game_view = GameView(self.screen)

    def run(self):
        """Draw and get events."""
        self.clock.tick(FPS)
        self._get_events()

        if self.playing and self.game_view:
            self.game_view.update()

        self._draw()

    def _get_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        for event in pg.event.get():
            self.event = event
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        if self.playing and self.game_view:
            self.screen.fill(Color.sky)
            self.game_view.draw()
        else:
            self.screen.fill(Color.aqua)

            if self.page_state == "PLAYING":
                self.playing = True
            elif self.page_state == "OPTIONS":
                self.page_state = self.options.draw(
                    self.mouse_x, self.mouse_y, self.event
                )
            elif self.page_state == "QUIT":
                self.running = False
            else:
                self.page_state = self.main_menu.draw(
                    self.mouse_x, self.mouse_y, self.event
                )

        pg.display.flip()
