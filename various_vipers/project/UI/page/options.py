"""
Options page.

Handling input and making changes.
"""

import pygame as pg
from pygame.image import load

from project.UI.element.button import Button
from project.UI.element.slider import Slider
from project.UI.element.vol_indicator import VolumeIndicator
from project.constants import (
    BACK_BTN,
    BACK_BTN_HOVER,
    ButtonProperties,
    Color,
    VOLUME_BTN,
    VOLUME_BTN_MUTE,
    VOLUME_BTN_HOVER,
    VOLUME_BTN_MUTE_HOVER,
    WindowState,
)


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        back_btn_img = load(str(BACK_BTN)).convert_alpha()
        back_btn_img_hover = load(str(BACK_BTN_HOVER)).convert_alpha()

        vol_btn_img = load(str(VOLUME_BTN)).convert_alpha()
        vol_btn_img_hover = load(str(VOLUME_BTN_HOVER)).convert_alpha()

        vol_btn_img_mute = load(str(VOLUME_BTN_MUTE)).convert_alpha()
        vol_btn_img_mute_hover = load(str(VOLUME_BTN_MUTE_HOVER)).convert_alpha()

        self.back_btn = Button(
            self.screen,
            x=ButtonProperties.back_btn_x,
            y=ButtonProperties.back_btn_y,
            width=ButtonProperties.back_btn_w,
            height=ButtonProperties.back_btn_h,
            image=back_btn_img,
            image_hover=back_btn_img_hover,
        )

        self.vol_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=vol_btn_img,
            image_hover=vol_btn_img_hover,
        )

        self.vol_btn_mute = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=vol_btn_img_mute,
            image_hover=vol_btn_img_mute_hover,
        )
        self.slider = Slider(self.screen)
        self.volume_indicator = VolumeIndicator(self.screen)

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.aqua)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.main_menu
        else:
            self.back_btn.draw()

        if self.slider.volume == 0:
            if self.vol_btn_mute.rect.collidepoint(mouse_x, mouse_y):
                self.vol_btn_mute.draw(hover=True)

                if event.type == pg.MOUSEBUTTONDOWN:
                    return WindowState.main_menu
            else:
                self.vol_btn_mute.draw()
        else:
            if self.vol_btn.rect.collidepoint(mouse_x, mouse_y):
                self.vol_btn.draw(hover=True)

                if event.type == pg.MOUSEBUTTONDOWN:
                    return WindowState.main_menu
            else:
                self.vol_btn.draw()

        self.slider.move_indicator(mouse_x, mouse_y, event)
        self.slider.draw()

        self.volume_indicator.volume = self.slider.volume
        self.volume_indicator.draw()

        return WindowState.options
