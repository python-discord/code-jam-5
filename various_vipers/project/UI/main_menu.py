"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg

from project.UI.button import generate_buttons
from project.constants import (
    Button,
    OPT_BTN,
    OPT_BTN_HOVER,
    PLAY_BTN,
    PLAY_BTN_HOVER,
    QUIT_BTN,
    QUIT_BTN_HOVER,
)


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        """Set initial main menu values."""
        self.screen = screen

        self.play_btn_img = pg.image.load(str(PLAY_BTN)).convert_alpha()
        self.play_btn_img_h = pg.image.load(str(PLAY_BTN_HOVER))

        self.opt_btn_img = pg.image.load(str(OPT_BTN))
        self.opt_btn_img_h = pg.image.load(str(OPT_BTN_HOVER))

        self.quit_btn_img = pg.image.load(str(QUIT_BTN))
        self.quit_btn_img_h = pg.image.load(str(QUIT_BTN_HOVER))

        self.play_btn, self.opt_btn, self.quit_btn = generate_buttons(
            btn_w=Button.main_btn_w,
            btn_h=Button.main_btn_h,
            btn_count=3,
            gap=Button.btn_gap,
        )

    def draw(self, mouse_x: int, mause_y: int, mouse_click: bool):
        """Hadle all main menu events."""
        self.play_btn.draw(self.screen, False, self.play_btn_img)
        self.opt_btn.draw(self.screen, False, self.opt_btn_img)
        self.quit_btn.draw(self.screen, False, self.quit_btn_img)

    # def draw(self,):
    #     """Draw all main menu elements."""
    #     pg.draw.rect(self.screen, Color.white, self.play_btn.rect)
    #     pg.draw.rect(self.screen, Color.white, self.opt_btn.rect)
    #     pg.draw.rect(self.screen, Color.white, self.quit_btn.rect)
