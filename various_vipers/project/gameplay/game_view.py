import logging
import time
from typing import List

import pygame as pg

from project.UI.element.button import Button
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS,
    Color,
    HEIGHT,
    MAX_HEAT,
    PAUSE_WINDOW,
    WIDTH,
    WindowState,
)
from project.utils.helpers import load_img
from .game_state import GameState
from .period import PeriodFuture, PeriodMedieval, PeriodModern


logger = logging.getLogger(__name__)
game_vars = GameState()


class GameView:
    """GameView hold the information about all things related to the main game."""

    # Background images that will be looping
    BG_images: List[str] = []

    # Delay before repeated pausing/unpausing of the game
    pause_start: float = 0

    def __init__(self, screen: pg.Surface, difficulty: int = 1):
        """
        Initializer for GameView class.

        screen - parent screen to draw objects on
        difficulty - 0, 1, 2. Difficulty increases with number.
        """
        self.screen = screen

        # Pause window
        self.window_rect = pg.Rect(
            int(WIDTH * 0.375), int(HEIGHT * 0.2), int(WIDTH * 0.25), int(HEIGHT * 0.5)
        )
        self.window_image = load_img(PAUSE_WINDOW)
        self.window_image = pg.transform.scale(self.window_image, self.window_rect.size)

        btn_height = 80
        btn_offset_x = 20
        btn_offset_y = 50

        exit_btn_image = load_img(BUTTONS["exit-btn"])
        exit_btn_hover = load_img(BUTTONS["exit-btn-hover"])
        self.exit_btn = Button(
            self.screen,
            self.window_rect.x + btn_offset_x,
            self.window_rect.y + self.window_rect.height - btn_height - btn_offset_y,
            self.window_rect.width - btn_offset_x * 2,
            btn_height,
            exit_btn_image,
            exit_btn_hover,
        )

        resume_btn_image = load_img(BUTTONS["resume-btn"])
        resume_btn_hover = load_img(BUTTONS["resume-btn-hover"])
        self.resume_btn = Button(
            self.screen,
            self.window_rect.x + btn_offset_x,
            self.exit_btn.rect.y - btn_height - btn_offset_y // 2,
            self.window_rect.width - btn_offset_x * 2,
            btn_height,
            resume_btn_image,
            resume_btn_hover,
        )

        if difficulty == 0:
            self.period = PeriodMedieval(self.screen)
        elif difficulty == 1:
            self.period = PeriodModern(self.screen)
        elif difficulty == 2:
            self.period = PeriodFuture(self.screen)
        else:
            raise TypeError(f"Unknown difficulty level passed: {difficulty}")

    def update(self, event: pg.event) -> None:
        """Update gets called every game tick."""
        if (
            game_vars.is_started
            and game_vars.open_task is None
            and pg.key.get_pressed()[pg.K_ESCAPE]
            and time.time() > self.pause_start + 0.3
        ):
            game_vars.is_paused = not game_vars.is_paused
            self.pause_start = time.time()

        if not game_vars.is_paused:
            self.period.update(event)

    def draw(self, event: pg.event) -> WindowState:
        """
        Draw main screen / period / difficulty of the game.

        Returns GameOver WindowState if condition is met; else None.
        """
        # Check for gameover condition
        if game_vars.current_heat >= MAX_HEAT:
            Sound.game_over.play()
            return WindowState.gameover

        self.period.draw()

        if game_vars.is_paused:
            self._draw_pause_window(event)

        return None

    def _draw_pause_window(self, event: pg.event) -> None:
        self.screen.blit(self.window_image, self.window_rect)

        font = pg.font.Font(None, 60)
        font.set_bold(True)
        pause_text = font.render("PAUSED", True, Color.white)
        text_x = (
            self.window_rect.x
            + (self.window_rect.width // 2)
            - (pause_text.get_width() // 2)
        )
        text_y = self.window_rect.y + 25
        self.screen.blit(pause_text, (text_x, text_y))

        self._draw_buttons(event)

    def _draw_buttons(self, event: pg.event) -> None:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.resume_btn.rect.collidepoint(mouse_x, mouse_y):
            self.resume_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                Sound.click.play()
                game_vars.is_paused = False
        else:
            self.resume_btn.draw()

        if self.exit_btn.rect.collidepoint(mouse_x, mouse_y):
            self.exit_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                Sound.click.play()
                game_vars.reset_game = True
        else:
            self.exit_btn.draw()
