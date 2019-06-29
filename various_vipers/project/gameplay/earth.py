import logging

import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import BG_SCROLL_SPEED, HEIGHT, WIDTH


logger = logging.getLogger(__name__)


class Earth(object):
    """
    Represent Earth class object.

    Includes logic for handling background and game tasks.
    """

    current_position = 0

    def __init__(self, screen, bg_images, tilemap):
        self.screen = screen
        self.tilemap = tilemap

        # preload and scale all bg images
        new_size = int(HEIGHT * 0.8)
        self.bg_images = [
            scale(load(str(image)), (new_size, new_size)) for image in bg_images
        ]

        # Calculate max position by added the width of all bg images
        self.max_position = sum(image.get_width() for image in self.bg_images)

    def update(self):
        """Update game logic with each game tick."""
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            self.__scroll_left()
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            self.__scroll_right()

    def draw(self):
        """Draw all images related to the earth."""
        self.__draw_background()

    def __draw_background(self):
        i, image_x = self.__find_first_bg_image()
        # From the first BG image, draw new images to the right, until whole screen is filled
        while True:
            if i > len(self.bg_images) - 1:
                # Loop images
                i = 0

            image = self.bg_images[i]
            self.screen.blit(image, (image_x, HEIGHT // 5))

            image_x += image.get_width()
            if image_x > WIDTH:
                break

            i += 1

    def __find_first_bg_image(self):
        """
        Function returns index, and position of first BG image that should be drawn on the left.

        Screen and individual images widths are taken into account when finding the first image.
        """
        _position = 0
        i = 0
        while i < len(self.bg_images):
            image = self.bg_images[i]

            if _position - self.current_position + image.get_width() > 0:
                break

            _position += image.get_width()
            i += 1

        return (i, _position - self.current_position)

    def __scroll_left(self):
        logger.debug("Scrolling LEFT.")
        self.current_position -= BG_SCROLL_SPEED
        self.__update_position()

    def __scroll_right(self):
        logger.debug("Scrolling RIGHT.")
        self.current_position += BG_SCROLL_SPEED
        self.__update_position()

    def __update_position(self):
        if self.current_position > self.max_position:
            self.current_position = 0
        elif self.current_position < 0:
            self.current_position = self.max_position
        # logger.debug(self.current_position)
