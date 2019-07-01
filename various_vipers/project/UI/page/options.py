"""
Options page.

Handling input and making changes.
"""

import pygame as pg

from project.UI.element.button import Button
from project.UI.element.slider import Slider
from project.constants import (
    BACK_BTN,
    BACK_BTN_HOVER,
    ButtonProperties,
    Color,
    WindowState,
)


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        back_btn_img = pg.image.load(str(BACK_BTN)).convert_alpha()
        back_btn_img_hover = pg.image.load(str(BACK_BTN_HOVER)).convert_alpha()

        self.back_btn = Button(
            x=ButtonProperties.back_btn_x,
            y=ButtonProperties.back_btn_y,
            width=ButtonProperties.back_btn_w,
            height=ButtonProperties.back_btn_h,
            image=back_btn_img,
            image_hover=back_btn_img_hover,
        )
        self.slider = Slider()

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.aqua)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(self.screen, hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.main_menu
        else:
            self.back_btn.draw(self.screen)

        self.slider.move_indicator(mouse_x, mouse_y, event)
        self.slider.draw(self.screen)
        return WindowState.options
