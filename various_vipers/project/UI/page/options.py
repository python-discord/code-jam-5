"""
Options page.

Handling input and making changes.
"""
import logging
import time

import pygame as pg

from project.UI.element.button import Button
from project.UI.element.slider import Slider
from project.UI.element.vol_indicator import VolumeIndicator
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    HEIGHT,
    PATH_OPTIONS_BG,
    WIDTH,
    WindowState,
)
from project.utils.helpers import draw_infinity_bg, load_img
from project.utils.user_data import UserData


logger = logging.getLogger(__name__)
user_data = UserData()
user_data.load()


class Options:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.event = None

        self.bg_rect_1 = pg.Rect(0, 0, WIDTH, HEIGHT)
        self.bg_rect_2 = pg.Rect(-WIDTH, 0, WIDTH, HEIGHT)

        self.background = load_img(PATH_OPTIONS_BG)

        back_btn_img = load_img(BTN["back-btn"])
        back_btn_img_hover = load_img(BTN["back-btn-hover"])

        vol_btn_img = load_img(BTN["vol-btn"])
        vol_btn_img_hover = load_img(BTN["vol-btn-hover"])

        vol_btn_img_mute = load_img(BTN["vol-btn-mute"])
        vol_btn_img_mute_hover = load_img(BTN["vol-btn-mute-hover"])

        checker_btn = load_img(BTN["checker"])
        checker_btn_hover = load_img(BTN["checker-hover"])

        checker_btn_checked = load_img(BTN["checker-checked"])
        checker_btn_checked_hover = load_img(BTN["checker-checked-hover"])

        fps_label_img = load_img(BTN["show-fps-label"])
        boost_fps_label_img = load_img(BTN["boost-fps-label"])

        sound_label_img = load_img(BTN["sound-label"])
        music_label_img = load_img(BTN["music-label"])

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
            y=ButtonProperties.vol_btn_y + 260,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn,
            image_hover=checker_btn_hover,
        )

        self.fps_checker_checked_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 260,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn_checked,
            image_hover=checker_btn_checked_hover,
        )

        self.boost_fps_checker_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 390,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn,
            image_hover=checker_btn_hover,
        )

        self.boost_fps_checker_checked_btn = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 390,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=checker_btn_checked,
            image_hover=checker_btn_checked_hover,
        )

        self.fps_label = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x + 100,
            y=ButtonProperties.vol_btn_y + 260,
            width=500,
            height=100,
            image=fps_label_img,
            image_hover=fps_label_img,
        )

        self.boost_fps_label = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x + 100,
            y=ButtonProperties.vol_btn_y + 390,
            width=500,
            height=100,
            image=boost_fps_label_img,
            image_hover=boost_fps_label_img,
        )

        self.vol_btn2 = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 130,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=vol_btn_img,
            image_hover=vol_btn_img_hover,
        )

        self.vol_btn_mute2 = Button(
            self.screen,
            x=ButtonProperties.vol_btn_x,
            y=ButtonProperties.vol_btn_y + 130,
            width=ButtonProperties.vol_btn_w,
            height=ButtonProperties.vol_btn_h,
            image=vol_btn_img_mute,
            image_hover=vol_btn_img_mute_hover,
        )

        self.sound_label = Button(
            self.screen,
            x=WIDTH - 300,
            y=self.vol_btn.rect.top,
            width=300,
            height=100,
            image=sound_label_img,
            image_hover=sound_label_img,
        )

        self.music_label = Button(
            self.screen,
            x=WIDTH - 300,
            y=self.vol_btn2.rect.top,
            width=300,
            height=100,
            image=music_label_img,
            image_hover=music_label_img,
        )
        self.last_click = int()

        self.slider = Slider(self.screen, 1)
        self.volume_indicator = VolumeIndicator(self.screen, 1)

        self.slider2 = Slider(self.screen, 2)
        self.volume_indicator2 = VolumeIndicator(self.screen, 2)

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadle all options events and draw elements."""
        self.event = event
        self.mouse_x, self.mouse_y = mouse_x, mouse_y

        draw_infinity_bg(self.screen, self.background, self.bg_rect_1, self.bg_rect_2)

        if self.back_btn.rect.collidepoint(mouse_x, mouse_y):
            self.back_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                Sound.click.play()
                user_data.save()
                return WindowState.main_menu
        else:
            self.back_btn.draw()

        self.__draw_volume_button(self.vol_btn, self.vol_btn_mute, self.slider)
        self.__draw_volume_button(self.vol_btn2, self.vol_btn_mute2, self.slider2)

        self.__draw_fps_checker_button()
        self.__draw_boost_fps_checker_button()

        self.slider.move_indicator(mouse_x, mouse_y, event)
        self.slider.draw()

        self.slider2.move_indicator(mouse_x, mouse_y, event)
        self.slider2.draw()

        self.volume_indicator.volume = self.slider.volume
        self.volume_indicator2.volume = self.slider2.volume

        self.volume_indicator.draw()
        self.volume_indicator2.draw()

        self.fps_label.draw()
        self.boost_fps_label.draw()
        self.sound_label.draw()
        self.music_label.draw()
        return WindowState.options

    def __draw_volume_button(
        self, vol: Button, vol_mute: Button, slider: Slider
    ) -> None:
        """
        Draws the volume button of the two sliders.

        The volume buttons mute the volume.
        """
        clicked = self.event.type == pg.MOUSEBUTTONDOWN

        if slider.number == 1:
            mute = user_data.sound_mute = slider.volume == 0
        else:
            mute = user_data.music_mute = slider.volume == 0

        if mute:
            if vol_mute.rect.collidepoint(self.mouse_x, self.mouse_y):
                vol_mute.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()

                    slider.volume = 5
                    slider.update()

                    if slider.number == 1:
                        user_data.sound_volume = 5
                        user_data.sound_mute = False
                    else:
                        user_data.music_volume = 5
                        user_data.music_mute = False
                    Sound.update()
            else:
                vol_mute.draw()
        else:
            if vol.rect.collidepoint(self.mouse_x, self.mouse_y):
                vol.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()

                    slider.volume = 0
                    slider.update()

                    if slider.number == 1:
                        user_data.sound_mute = True
                    else:
                        user_data.music_mute = True
                    Sound.update()
            else:
                vol.draw()

    def __draw_fps_checker_button(self) -> None:
        """
        Draw the fps checker button.

        Which toggle the displaying of the FPS.
        """
        clicked = self.event.type == pg.MOUSEBUTTONDOWN

        if user_data.show_fps:
            if self.fps_checker_checked_btn.rect.collidepoint(
                self.mouse_x, self.mouse_y
            ):
                self.fps_checker_checked_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()
                    user_data.show_fps = False
            else:
                self.fps_checker_checked_btn.draw()
        else:
            if self.fps_checker_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
                self.fps_checker_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()
                    user_data.show_fps = True
            else:
                self.fps_checker_btn.draw()

    def __draw_boost_fps_checker_button(self) -> None:
        """
        Draw the boost fps checker button.

        Which toggle the boosting of the FPS.
        With removing some animations in the game to increase performance.
        """
        clicked = self.event.type == pg.MOUSEBUTTONDOWN

        if user_data.boost_fps:
            if self.boost_fps_checker_checked_btn.rect.collidepoint(
                self.mouse_x, self.mouse_y
            ):
                self.boost_fps_checker_checked_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()
                    user_data.boost_fps = False
            else:
                self.boost_fps_checker_checked_btn.draw()
        else:
            if self.boost_fps_checker_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
                self.boost_fps_checker_btn.draw(hover=True)

                if clicked and (time.time() - self.last_click) > 0.3:
                    Sound.click.play()
                    self.last_click = time.time()
                    user_data.boost_fps = True
            else:
                self.boost_fps_checker_btn.draw()
