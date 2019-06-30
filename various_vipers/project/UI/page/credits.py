"""
Credits page.

Handling input and making changes.
"""

import pygame as pg

from project.UI.element.button import ButtonModel
from project.constants import BACK_BTN, BACK_BTN_HOVER, Color, WindowState


class Credits:
    """Represents Credits page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        back_btn_img = pg.image.load(str(BACK_BTN)).convert_alpha()
        back_btn_img_h = pg.image.load(str(BACK_BTN_HOVER)).convert_alpha()

        self.back_btn = ButtonModel(
            x=20,
            y=20,
            width=200,
            height=100,
            image=back_btn_img,
            image_hover=back_btn_img_h,
        )

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.aqua)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(self.screen, hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.main_menu
        else:
            self.back_btn.draw(self.screen)
        return WindowState.credit
