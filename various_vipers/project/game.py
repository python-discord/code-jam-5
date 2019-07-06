"""Game model."""
import logging

import pygame as pg

from project.UI.fx.sound import Sound
from project.UI.page.credits import Credits
from project.UI.page.gameover import GameOver
from project.UI.page.main_menu import MainMenu
from project.UI.page.options import Options
from project.constants import Color, FPS, HEIGHT, WIDTH, WindowState
from project.gameplay.game_state import GameState
from project.gameplay.game_view import GameView
from project.utils.user_data import UserData


logger = logging.getLogger(__name__)
game_vars = GameState()
user_data = UserData()


class Game:
    """Represents main game class."""

    def __init__(self):
        """Set initial values."""
        pg.init()
        user_data.load()
        Sound.update()

        pg.display.set_caption("Various Vipers game in development")

        self.running = True

        self.mouse_x = self.mouse_y = int()
        self.event = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.main_menu = MainMenu(self.screen)
        self.options = Options(self.screen)
        self.credits = Credits(self.screen)
        self.gameover = GameOver(self.screen)
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

        # Will either be gameover or current window state
        self.window_state = self.game_view.draw(self.event) or self.window_state

        if self.window_state == WindowState.main_menu:
            self.window_state = self.main_menu.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.options:
            self.window_state = self.options.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.credit:
            self.window_state = self.credits.draw(
                self.mouse_x, self.mouse_y, self.event
            )
        elif self.window_state == WindowState.gameover:
            game_vars.is_started = False
            self.window_state == self.gameover.draw(
                self.mouse_x, self.mouse_y, self.event, self.game_view.period
            )
        elif self.window_state == WindowState.quited:
            self.running = False
        elif self.window_state == WindowState.game:
            game_vars.is_started = True

        if user_data.show_fps:
            self._draw_fps()

        pg.display.flip()

    def _draw_fps(self) -> None:
        font = pg.font.Font(None, 50)
        fps_indicator = font.render(str(int(self.clock.get_fps())), True, Color.orange)
        self.screen.blit(fps_indicator, (WIDTH - fps_indicator.get_width(), 0))
