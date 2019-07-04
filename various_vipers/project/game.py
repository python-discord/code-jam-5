"""Game model."""
import logging

import pygame as pg

from project.UI.page.credits import Credits
from project.UI.page.main_menu import MainMenu
from project.UI.page.options import Options
from project.constants import BG_MUSIC, Color, FPS, HEIGHT, WIDTH, WindowState
from project.gameplay.game_view import GameView
from project.tools.loader import Load


logger = logging.getLogger(__name__)


class Game:
    """Represents main game class."""

    def __init__(self):
        """Set initial values."""
        pg.init()
        pg.mixer.init()

        pg.mixer.music.load(str(BG_MUSIC))
        pg.mixer.music.play()

        pg.display.set_caption("Various Vipers game in development")

        self.running = True

        self.mouse_x = self.mouse_y = int()
        self.event = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.window_state = WindowState.main_menu

        self.main_menu = MainMenu(self.screen)
        self.options = Options(self.screen)
        self.credits = Credits(self.screen)
        self.game_view = GameView(self.screen)

        self.show_fps = Load.show_fps()

    def run(self):
        """Draw and get events."""
        self.clock.tick(FPS)
        self._get_events()

        self._draw()

    def _get_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        for event in pg.event.get():
            self.event = event
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        if self.window_state == WindowState.game:
            self.game_view.update(self.event)
            self.game_view.draw()
        else:
            self.screen.fill(Color.black)

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

        if self.show_fps:
            self._draw_fps()

        pg.display.flip()

    def _draw_fps(self):
        font = pg.font.Font(None, 50)
        fps_indicator = font.render(
            str(int(self.clock.get_fps())), True, pg.Color("red")
        )
        self.screen.blit(fps_indicator, (WIDTH - fps_indicator.get_width(), 0))
