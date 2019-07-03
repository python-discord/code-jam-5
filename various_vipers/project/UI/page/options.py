"""
Options page.

Handling input and making changes.
"""
import time

import pygame as pg
from pygame.image import load

from project.UI.element.button import Button
from project.UI.element.slider import Slider
from project.UI.element.vol_indicator import VolumeIndicator
from project.constants import (
    BUTTONS,
    ButtonProperties,
    Color,
    # VOLUME_BTN,
    # VOLUME_BTN_MUTE,
    # VOLUME_BTN_HOVER,
    # VOLUME_BTN_MUTE_HOVER,
    WindowState,
)


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        BTN = BUTTONS
        back_btn_img = pg.image.load(str(BTN["back-btn"])).convert_alpha()
        back_btn_img_hover = pg.image.load(str(BTN["back-btn-hover"])).convert_alpha()

        vol_btn_img = load(str(BTN["vol-btn"])).convert_alpha()
        vol_btn_img_hover = load(str(BTN["vol-btn-hover"])).convert_alpha()

        vol_btn_img_mute = load(str(BTN["vol-btn-mute"])).convert_alpha()
        vol_btn_img_mute_hover = load(str(BTN["vol-btn-mute-hover"])).convert_alpha()

        checker_btn = load(str(BTN["checker"])).convert_alpha()
        checker_btn_hover = load(str(BTN["checker-hover"])).convert_alpha()

        fps_label_img = load(str(BTN["show-fps-label"])).convert_alpha()

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

        self.fps_checker_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 130,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn,
            image_hover=checker_btn_hover,
        )

        self.fps_label = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x + 100,
            y=ButtonProperties.vol_btn_y + 130,
            width=500,
            height=100,
            image=fps_label_img,
            image_hover=fps_label_img,
        )
        self.slider = Slider(self.screen)
        self.volume_indicator = VolumeIndicator(self.screen)

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.screen.fill(Color.black)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.main_menu
        else:
            self.back_btn.draw()

        mute = self.slider.volume == 0
        if mute:
            if self.vol_btn_mute.rect.collidepoint(mouse_x, mouse_y):
                self.vol_btn_mute.draw(hover=True)

                if event.type == pg.MOUSEBUTTONDOWN and mute:
                    self.slider.volume = 5
                    self.slider.update()
                    mute = False
            else:
                self.vol_btn_mute.draw()
        else:
            if self.vol_btn.rect.collidepoint(mouse_x, mouse_y):
                self.vol_btn.draw(hover=True)

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.slider.volume = 0
                    self.slider.update()
                    time.sleep(0.1)
            else:
                self.vol_btn.draw()

        if self.fps_checker_btn.rect.collidepoint(mouse_x, mouse_y):
            self.fps_checker_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                return WindowState.main_menu
        else:
            self.fps_checker_btn.draw()

        self.slider.move_indicator(mouse_x, mouse_y, event)
        self.slider.draw()

        self.volume_indicator.volume = self.slider.volume
        self.volume_indicator.draw()

        self.fps_label.draw()
        return WindowState.options
