"""Contains a slider model."""

import pygame as pg
from pygame import Rect

from project.constants import WIDTH
from project.tools.loader import get_volume, save_volume


class Slider:
    """Represents a volume slider."""

    def __init__(
        self,
        # image: pg.image,
        # image_hover: pg.image,
    ):
        """Sets rectangle object for the slider."""
        # self.image = image
        # self.image_hover = image_hover

        self.volume = get_volume()

        self.x = WIDTH * 0.2
        y = 200
        self.width = WIDTH - (WIDTH * 0.2) - self.x
        height = 10

        self.indicator_pos = (self.width / 100) * self.volume

        self.x_i = self.x + self.indicator_pos
        self.y_i = 200 - 30

        self.width_i = 20
        self.height_i = 60

        self.slider_body = Rect(self.x, y, self.width, height)
        self.slider_indicator = Rect(self.x_i, self.y_i, self.width_i, self.height_i)

        self.click = False

    def draw(self, screen: pg.Surface) -> None:
        """Draws the slider on the screen."""
        pg.draw.rect(screen, (255, 0, 0), self.slider_body)
        pg.draw.rect(screen, (0, 255, 0), self.slider_indicator)
        # if hover:
        #     screen.blit(self.image_hover, self.rect)
        # else:
        #     screen.blit(self.image, self.rect)

    def move_indicator(self, x, y, event) -> None:
        """Moves the indicator on the x axis if mouse is pressed."""
        b = pg.mouse.get_pressed()[0]

        if b and self.click:
            if x > self.x and x < WIDTH - (WIDTH * 0.2):
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
