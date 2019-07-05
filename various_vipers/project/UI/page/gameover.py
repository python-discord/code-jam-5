"""
GameOver page.

Handling input and making changes.
"""
import logging

import pygame as pg

from project.UI.element.button import Button
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    HEIGHT,
    PATH_GAMEOVER_BG,
    WIDTH,
    WindowState,
)
from project.gameplay.game_state import GameState


logger = logging.getLogger(__name__)
game_vars = GameState()


class GameOver:
    """Represents GameOver page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        home_btn_img = pg.image.load(str(BTN["main-menu-btn"])).convert_alpha()
        home_btn_img_h = pg.image.load(str(BTN["main-menu-btn-hover"])).convert_alpha()

        self.background = pg.image.load(str(PATH_GAMEOVER_BG)).convert_alpha()

        self.bg_rect_1 = pg.Rect(0, 0, WIDTH, HEIGHT)
        self.bg_rect_2 = pg.Rect(-WIDTH, 0, WIDTH, HEIGHT)

        self.home_btn = Button(
            screen=self.screen,
            x=ButtonProperties.back_btn_x,
            y=ButtonProperties.back_btn_y,
            width=ButtonProperties.back_btn_w,
            height=ButtonProperties.back_btn_h,
            image=home_btn_img,
            image_hover=home_btn_img_h,
        )

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.__draw_infinity_bg()

        if self.home_btn.rect.collidepoint(mouse_x, mouse_y):
            self.home_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                Sound.click.play()
                game_vars.reset_game = True
        else:
            self.home_btn.draw()
        return WindowState.gameover

    def __draw_infinity_bg(self):
        self.bg_rect_1.left += 1
        self.bg_rect_2.left += 1

        if self.bg_rect_1.left == WIDTH:
            self.bg_rect_1.left = -WIDTH
        if self.bg_rect_2.left == WIDTH:
            self.bg_rect_2.left = -WIDTH

        self.screen.blit(self.background, self.bg_rect_1)
        self.screen.blit(self.background, self.bg_rect_2)
