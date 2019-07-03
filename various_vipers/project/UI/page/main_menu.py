"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg
from pygame.image import load

from project.UI.element.button import generate_main_buttons
from project.constants import (
    BUTTONS,
    ButtonProperties,
    MAIN_MENU_BG,
    WindowState,
    WIDTH,
    HEIGHT,
)


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        """Set initial main menu values."""
        self.screen = screen

        self.background = load(str(MAIN_MENU_BG)).convert_alpha()

        self.__load_images()
        self.__create_buttons()
        self.__store_buttons_and_states()

    def __load_images(self):
        BTN = BUTTONS
        img_paths = [
            (BTN["play-btn"], BTN["play-btn-hover"]),
            (BTN["options-btn"], BTN["options-btn-hover"]),
            (BTN["credits-btn"], BTN["credits-btn-hover"]),
            (BTN["quit-btn"], BTN["quit-btn-hover"]),
        ]

        # load two types of images for the buttons
        # normal state and hover state
        self.images = [
            tuple([load(str(j)).convert_alpha() for j in i]) for i in img_paths
        ]

    def __create_buttons(self):
        self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn = generate_main_buttons(
            screen=self.screen,
            btn_w=ButtonProperties.main_btn_w,
            btn_h=ButtonProperties.main_btn_h,
            btn_count=4,
            gap=ButtonProperties.btn_gap,
            images=self.images,
        )

    def __store_buttons_and_states(self):
        self.buttons = [self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn]
        self.states = [
            WindowState.game,
            WindowState.options,
            WindowState.credit,
            WindowState.quited,
        ]

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadles all main menu events and draw every elements."""
        self.screen.blit(self.background, (0, 0, WIDTH, HEIGHT))

        # hover check for the play button
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):
                button.draw(hover=True)
                if event.type == pg.MOUSEBUTTONDOWN:
                    return self.states[i]
            else:
                button.draw()
        return WindowState.main_menu
