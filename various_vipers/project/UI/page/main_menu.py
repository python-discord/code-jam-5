"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg

from project.UI.element.button import generate_main_buttons
from project.constants import (
    Button,
    OPT_BTN,
    OPT_BTN_HOVER,
    PLAY_BTN,
    PLAY_BTN_HOVER,
    QUIT_BTN,
    QUIT_BTN_HOVER,
    WindowState,
)


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        """Set initial main menu values."""
        self.screen = screen

        # load two types of images for the buttons
        # normal state and hover state
        self.play_btn_img = pg.image.load(str(PLAY_BTN)).convert_alpha()
        self.play_btn_img_h = pg.image.load(str(PLAY_BTN_HOVER)).convert_alpha()

        self.opt_btn_img = pg.image.load(str(OPT_BTN)).convert_alpha()
        self.opt_btn_img_h = pg.image.load(str(OPT_BTN_HOVER)).convert_alpha()

        self.quit_btn_img = pg.image.load(str(QUIT_BTN)).convert_alpha()
        self.quit_btn_img_h = pg.image.load(str(QUIT_BTN_HOVER)).convert_alpha()

        # generates buttons objects
        self.play_btn, self.opt_btn, self.quit_btn = generate_main_buttons(
            btn_w=Button.main_btn_w,
            btn_h=Button.main_btn_h,
            btn_count=3,
            gap=Button.btn_gap,
        )
        self.buttons = [self.play_btn, self.opt_btn, self.quit_btn]
        self.states = [WindowState.game, WindowState.options, WindowState.quited]
        self.images = [
            # normal state   &    hover state
            (self.play_btn_img, self.play_btn_img_h),
            (self.opt_btn_img, self.opt_btn_img_h),
            (self.quit_btn_img, self.quit_btn_img_h),
        ]

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadles all main menu events and draw every elements."""
        # hover check for the play button
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):
                button.draw(self.screen, self.images[i][1])
                if event.type == pg.MOUSEBUTTONDOWN:
                    return self.states[i]
            else:
                button.draw(self.screen, self.images[i][0])
        return WindowState.main_menu
