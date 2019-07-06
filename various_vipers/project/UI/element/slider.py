"""Contains a slider model."""

import pygame as pg
from pygame import Rect
from pygame.image import load

from project.UI.fx.sound import Sound
from project.constants import SLIDER_BODY, SLIDER_INDICATOR, SliderProperties
from project.utils.user_data import UserData


user_data = UserData()


class Slider:
    """Represents a volume slider."""

    def __init__(self, screen: pg.Surface, number):
        """Sets rectangle object for the slider."""
        self.screen = screen
        self.number = number

        if self.number == 1:
            self.volume = user_data.sound_volume
        else:
            self.volume = user_data.music_volume

        self.body_img = load(str(SLIDER_BODY)).convert_alpha()
        self.indicator_img = load(str(SLIDER_INDICATOR)).convert_alpha()

        self.__calculate_body_properties()
        self.__calculate_indicator_properties()
        self.__create_rectangles()

        self.click = False

    def __calculate_body_properties(self):
        self.x = SliderProperties.body_x
        self.y = SliderProperties.body_y
        self.width = SliderProperties.body_width
        self.height = SliderProperties.body_height

        if self.number == 2:
            self.y += 120

    def __calculate_indicator_properties(self):
        self.indicator_pos = (self.width / 100) * self.volume

        self.x_i = self.x + self.indicator_pos
        self.y_i = SliderProperties.body_y - (SliderProperties.indicator_h / 2)

        self.width_i = SliderProperties.indicator_w
        self.height_i = SliderProperties.indicator_h

        if self.number == 2:
            self.y_i += 120

    def __create_rectangles(self):
        self.slider_body = Rect(self.x, self.y, self.width, self.height)
        self.slider_indicator = Rect(self.x_i, self.y_i, self.width_i, self.height_i)

    def draw(self) -> None:
        """Draws the slider on the screen."""
        self.screen.blit(self.body_img, self.slider_body)
        self.screen.blit(self.indicator_img, self.slider_indicator)

    def move_indicator(self, x, y, event) -> None:
        """Moves the indicator on the x axis and saves the changes."""
        b = pg.mouse.get_pressed()[0]

        if b and self.click:
            if (
                x > self.x
                and x
                < (SliderProperties.body_width + SliderProperties.body_x) - self.width_i
            ):
                self.x_i = x
                self.slider_indicator = Rect(
                    self.x_i, self.y_i, self.width_i, self.height_i
                )

                self.volume = int(
                    (100 / (self.width - self.width_i - 3)) * (x - self.x)
                )

                if self.number == 1:
                    user_data.sound_volume = self.volume
                else:
                    user_data.music_volume = self.volume
                Sound.update()

        elif b:
            self.click = self.slider_body.collidepoint(
                x, y
            ) or self.slider_indicator.collidepoint(x, y)
        else:
            self.click = False

    def update(self):
        """Updates the slider indicator position after mute or unmute."""
        self.__calculate_indicator_properties()
        self.slider_indicator = Rect(self.x_i, self.y_i, self.width_i, self.height_i)
