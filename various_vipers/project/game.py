"""Game model."""
import logging

import pygame as pg

from project.UI.page.credits import Credits
from project.UI.page.main_menu import MainMenu
from project.UI.page.options import Options
from project.constants import Color, FPS, HEIGHT, WIDTH, WindowState
from project.gameplay.game_state import GameState
from project.gameplay.game_view import GameView
from project.utils.loader import Load


logger = logging.getLogger(__name__)
game_vars = GameState()


class Game:
    """Represents main game class."""

    def __init__(self):
        """Set initial values."""
        pg.init()
        pg.mixer.init()

        pg.display.set_caption("Various Vipers game in development")

        self.running = True

        self.mouse_x = self.mouse_y = int()
        self.event = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.show_fps = Load.show_fps()

        self.main_menu = MainMenu(self.screen)
        self.options = Options(self.screen)
        self.credits = Credits(self.screen)
        self.reset()

    def reset(self) -> None:
        """Reset and reinitialize main game view."""
        if hasattr(self, "game_view"):
            game_vars.reset(self.game_view.period)

        self.window_state = WindowState.main_menu
        self.game_view = GameView(self.screen)

    def run(self):
        """Draw and get events."""
        self.clock.tick(FPS)
        self._get_events()
        self._draw()

        if game_vars.reset_game:
            self.reset()

    def _get_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        for event in pg.event.get():
            self.event = event
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        self.game_view.update(self.event)
        self.game_view.draw(self.event)

        if self.window_state == WindowState.main_menu:
            self.window_state = self.main_menu.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.options:
            self.window_state, self.show_fps = self.options.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.credit:
            self.window_state = self.credits.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.quited:
            self.running = False
        elif self.window_state == WindowState.game:
            game_vars.is_started = True

        if self.show_fps:
            self._draw_fps()

        pg.display.flip()

    def _draw_fps(self) -> None:
        font = pg.font.Font(None, 50)
        fps_indicator = font.render(str(int(self.clock.get_fps())), True, Color.orange)
        self.screen.blit(fps_indicator, (WIDTH - fps_indicator.get_width(), 0))
