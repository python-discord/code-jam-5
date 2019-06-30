"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg
from pygame.image import load

from project.UI.element.button import generate_main_buttons
from project.constants import (
    Button,
    CREDITS_BTN,
    CREDITS_BTN_HOVER,
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

        img_paths = [
            (PLAY_BTN, PLAY_BTN_HOVER),
            (OPT_BTN, OPT_BTN_HOVER),
            (CREDITS_BTN, CREDITS_BTN_HOVER),
            (QUIT_BTN, QUIT_BTN_HOVER),
        ]

        # load two types of images for the buttons
        # normal state and hover state
        self.images = [
            tuple([load(str(j)).convert_alpha() for j in i]) for i in img_paths
        ]

        # generates buttons objects
        self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn = generate_main_buttons(
            btn_w=Button.main_btn_w,
            btn_h=Button.main_btn_h,
            btn_count=4,
            gap=Button.btn_gap,
            images=self.images,
        )
        self.buttons = [self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn]
        self.states = [
            WindowState.game,
            WindowState.options,
            WindowState.credit,
            WindowState.quited,
        ]

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadles all main menu events and draw every elements."""
        # hover check for the play button
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):
                button.draw(self.screen, hover=True)
                if event.type == pg.MOUSEBUTTONDOWN:
                    return self.states[i]
            else:
                button.draw(self.screen)
        return WindowState.main_menu
