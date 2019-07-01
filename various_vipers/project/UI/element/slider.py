"""Contains a slider model."""

import pygame as pg
from pygame import Rect
from pygame.image import load

from project.constants import SLIDER_BODY, SLIDER_INDICATOR, SliderProperties, WIDTH
from project.tools.loader import get_volume, save_volume


class Slider:
    """Represents a volume slider."""

    def __init__(self,):
        """Sets rectangle object for the slider."""

        self.volume = get_volume()

        self.body_img = load(str(SLIDER_BODY)).convert_alpha()
        self.indicator_img = load(str(SLIDER_INDICATOR)).convert_alpha()

        self.__calculate_body_properties()
        self.__calculate_indicator_properties()
        self.__create_rectangles()

        self.click = False

        print(self.slider_body)
        print(self.slider_indicator)

    def __calculate_body_properties(self):
        self.x = WIDTH * SliderProperties.margin_y
        self.y = SliderProperties.body_y

        self.width = WIDTH - (WIDTH * SliderProperties.margin_y) - self.x
        self.height = SliderProperties.body_height

    def __calculate_indicator_properties(self):
        self.indicator_pos = (self.width / 100) * self.volume

        self.x_i = self.x + self.indicator_pos
        self.y_i = SliderProperties.body_y - (SliderProperties.indicator_h / 2)

        self.width_i = SliderProperties.indicator_w
        self.height_i = SliderProperties.indicator_h

    def __create_rectangles(self):
        self.slider_body = Rect(self.x, self.y, self.width, self.height)
        self.slider_indicator = Rect(self.x_i, self.y_i, self.width_i, self.height_i)

    def draw(self, screen: pg.Surface) -> None:
        """Draws the slider on the screen."""
        screen.blit(self.body_img, self.slider_body)
        screen.blit(self.indicator_img, self.slider_indicator)

    def move_indicator(self, x, y, event) -> None:
        """Moves the indicator on the x axis and saves the changes."""
        b = pg.mouse.get_pressed()[0]

        if b and self.click:
            if x > self.x and x < WIDTH - (WIDTH * SliderProperties.margin_y):
                self.x_i = x
                self.slider_indicator = Rect(
                    self.x_i, self.y_i, self.width_i, self.height_i
                )

                vol = int((100 / self.width) * (x - self.x))
                save_volume(vol)
        elif b:
            self.click = self.slider_body.collidepoint(
                x, y
            ) or self.slider_indicator.collidepoint(x, y)
        else:
            self.click = False
