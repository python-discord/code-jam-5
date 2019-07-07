"""
Main Menu page.

Handling input and creating new events.
"""
import logging
import time
import webbrowser

import pygame as pg

from project.UI.element.button import Button, generate_main_buttons
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    HEIGHT,
    REPO_LINK,
    WIDTH,
    WindowState,
)
from project.utils.helpers import load_img


logger = logging.getLogger(__name__)


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        """Set initial main menu values."""
        self.screen = screen

        self.__load_images()

        self.__create_buttons()
        self.__store_buttons_and_states()
        self.__load_set_github_button()

        self.last_click = int()

    def __load_images(self):
        img_paths = [
            (BTN["play-btn"], BTN["play-btn-hover"]),
            (BTN["options-btn"], BTN["options-btn-hover"]),
            (BTN["credits-btn"], BTN["credits-btn-hover"]),
            (BTN["quit-btn"], BTN["quit-btn-hover"]),
        ]

        # load two types of images for the buttons
        # normal state and hover state
        self.images = [tuple([load_img(j) for j in i]) for i in img_paths]

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadles all main menu events and draw every elements."""
        self.event = event
        self.mouse_x, self.mouse_y = mouse_x, mouse_y

        self.clicked = event.type == pg.MOUSEBUTTONDOWN
        # hover check for the play button
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_x, mouse_y):

                button.draw(hover=True)

                if self.clicked:
                    Sound.click.play()
                    return self.states[i]
            else:
                button.draw()
        self.__draw_github_button()

        return WindowState.main_menu

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

    def __load_set_github_button(self):
        image = load_img(BTN["github"])
        image_hover = load_img(BTN["github-hover"])

        self.github_btn = Button(
            screen=self.screen,
            x=WIDTH - 120,
            y=HEIGHT - 120,
            width=100,
            height=100,
            image=image,
            image_hover=image_hover,
        )

    def __draw_github_button(self):
        if self.github_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
            self.github_btn.draw(hover=True)
            if self.clicked and (time.time() - self.last_click) > 0.3:
                Sound.click.play()
                self.last_click = time.time()
                webbrowser.open(REPO_LINK)
        else:
            self.github_btn.draw()
