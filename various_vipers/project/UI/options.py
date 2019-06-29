"""
Options page.

Handling input and making changes.
"""

import pygame as pg

from project.UI.button import ButtonModel
from project.constants import BACK_BTN, BACK_BTN_HOVER, Color


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.back_btn = ButtonModel(20, 20, 200, 100)

        self.back_btn_img = pg.image.load(str(BACK_BTN)).convert_alpha()
        self.back_btn_img_h = pg.image.load(str(BACK_BTN_HOVER)).convert_alpha()

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.aqua)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(self.screen, self.back_btn_img_h)

            if event.type == pg.MOUSEBUTTONDOWN:
                return None
        else:
            self.back_btn.draw(self.screen, self.back_btn_img)
        return "OPTIONS"
