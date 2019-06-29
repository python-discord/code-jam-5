"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg

from project.UI.button import generate_main_buttons
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

        self.play_btn_img = pg.image.load(str(PLAY_BTN)).convert_alpha()
        self.play_btn_img_h = pg.image.load(str(PLAY_BTN_HOVER)).convert_alpha()

        self.opt_btn_img = pg.image.load(str(OPT_BTN)).convert_alpha()
        self.opt_btn_img_h = pg.image.load(str(OPT_BTN_HOVER)).convert_alpha()

        self.quit_btn_img = pg.image.load(str(QUIT_BTN)).convert_alpha()
        self.quit_btn_img_h = pg.image.load(str(QUIT_BTN_HOVER)).convert_alpha()

        self.play_btn, self.opt_btn, self.quit_btn = generate_main_buttons(
            btn_w=Button.main_btn_w,
            btn_h=Button.main_btn_h,
            btn_count=3,
            gap=Button.btn_gap,
        )

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadle all main menu events."""
        # hover check for the play button
        if self.play_btn.rect.collidepoint(mouse_x, mouse_y):
            self.play_btn.draw(self.screen, self.play_btn_img_h)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.game
        else:
            self.play_btn.draw(self.screen, self.play_btn_img)

        # hover check for the options button
        if self.opt_btn.rect.collidepoint(mouse_x, mouse_y):
            self.opt_btn.draw(self.screen, self.opt_btn_img_h)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.options
        else:
            self.opt_btn.draw(self.screen, self.opt_btn_img)

        # hover check for the quit button
        if self.quit_btn.rect.collidepoint(mouse_x, mouse_y):
            self.quit_btn.draw(self.screen, self.quit_btn_img_h)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.quited
        else:
            self.quit_btn.draw(self.screen, self.quit_btn_img)

        return WindowState.main_menu
