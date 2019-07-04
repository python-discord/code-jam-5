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
    BUTTONS as BTN,
    ButtonProperties,
    Color,
    SOUNDS_BUTTONS as SND,
    WindowState,
)
from project.tools.loader import Load, Save


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.event = None

        self.__load_sounds()

        back_btn_img = pg.image.load(str(BTN["back-btn"])).convert_alpha()
        back_btn_img_hover = pg.image.load(str(BTN["back-btn-hover"])).convert_alpha()

        vol_btn_img = load(str(BTN["vol-btn"])).convert_alpha()
        vol_btn_img_hover = load(str(BTN["vol-btn-hover"])).convert_alpha()

        vol_btn_img_mute = load(str(BTN["vol-btn-mute"])).convert_alpha()
        vol_btn_img_mute_hover = load(str(BTN["vol-btn-mute-hover"])).convert_alpha()

        checker_btn = load(str(BTN["checker"])).convert_alpha()
        checker_btn_hover = load(str(BTN["checker-hover"])).convert_alpha()

        checker_btn_checked = load(str(BTN["checker-checked"])).convert_alpha()
        checker_btn_checked_hover = load(
            str(BTN["checker-checked-hover"])
        ).convert_alpha()

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

        self.fps_checker_checked_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 130,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn_checked,
            image_hover=checker_btn_checked_hover,
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
        self.mute = bool(Load.volume())
        self.fps_checked = Load.show_fps()

        self.last_click = int()
        self.slider = Slider(self.screen)
        self.volume_indicator = VolumeIndicator(self.screen)

    def draw(self, mouse_x: int, mouse_y: int, event):
        """Hadle all options events and draw elements."""
        self.event = event
        self.mouse_x, self.mouse_y = mouse_x, mouse_y

        self.screen.fill(Color.black)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                self.sounds["click"].play()
                return WindowState.main_menu, self.fps_checked
        else:
            self.back_btn.draw()

        self.__draw_volume_button()
        self.__draw_fps_checker_button()

        self.slider.move_indicator(mouse_x, mouse_y, event)
        self.slider.draw()

        self.volume_indicator.volume = self.slider.volume
        self.volume_indicator.draw()

        self.fps_label.draw()
        return WindowState.options, self.fps_checked

    def __load_sounds(self):
        self.sounds = {
            "click": pg.mixer.Sound(str(SND["click3"])),
            "check": pg.mixer.Sound(str(SND["switch1"])),
        }

    def __draw_volume_button(self):
        clicked = self.event.type == pg.MOUSEBUTTONDOWN
        self.mute = self.slider.volume == 0

        if self.mute:
            if self.vol_btn_mute.rect.collidepoint(self.mouse_x, self.mouse_y):
                self.vol_btn_mute.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    self.sounds["check"].play()
                    self.last_click = time.time()

                    self.slider.volume = 5
                    self.slider.update()

                    Save.volume(self.slider.volume)
                    self.mute = False
            else:
                self.vol_btn_mute.draw()
        else:
            if self.vol_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
                self.vol_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    self.sounds["check"].play()
                    self.last_click = time.time()

                    self.slider.volume = 0
                    self.slider.update()

                    Save.volume(self.slider.volume)
                    self.mute = True
            else:
                self.vol_btn.draw()

    def __draw_fps_checker_button(self):
        clicked = self.event.type == pg.MOUSEBUTTONDOWN

        if self.fps_checked:
            if self.fps_checker_checked_btn.rect.collidepoint(
                self.mouse_x, self.mouse_y
            ):
                self.fps_checker_checked_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    self.sounds["check"].play()
                    self.last_click = time.time()
                    self.fps_checked = False
                    Save.show_fps(self.fps_checked)
            else:
                self.fps_checker_checked_btn.draw()
        else:
            if self.fps_checker_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
                self.fps_checker_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    self.sounds["check"].play()
                    self.last_click = time.time()
                    self.fps_checked = True
                    Save.show_fps(self.fps_checked)
            else:
                self.fps_checker_btn.draw()
