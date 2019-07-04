"""
Credits page.

Handling input and making changes.
"""

import pygame as pg

from project.UI.element.button import Button
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    Color,
    SOUNDS_BUTTONS as SND,
    WindowState,
)


class Credits:
    """Represents Credits page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.__load_sounds()

        back_btn_img = pg.image.load(str(BTN["back-btn"])).convert_alpha()
        back_btn_img_h = pg.image.load(str(BTN["back-btn-hover"])).convert_alpha()

        self.back_btn = Button(
            screen=self.screen,
            x=ButtonProperties.back_btn_x,
            y=ButtonProperties.back_btn_y,
            width=ButtonProperties.back_btn_w,
            height=ButtonProperties.back_btn_h,
            image=back_btn_img,
            image_hover=back_btn_img_h,
        )

    def __load_sounds(self):
        self.sounds = {"click": pg.mixer.Sound(str(SND["click3"]))}

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.black)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                self.sounds["click"].play()
                return WindowState.main_menu
        else:
            self.back_btn.draw()
        return WindowState.credit
