import logging

import pygame as pg
from pygame.image import load

from project.constants import BG_SCROLL_SPEED


logger = logging.getLogger(__name__)


class Earth(object):
    current_position = 0

    def __init__(self, screen, bg_images, tilemap):
        self.screen = screen
        self.tilemap = tilemap
        # preload all bg images
        self.bg_images = [load(str(image)) for image in bg_images]

        # Calculate max position by added the width of all bg images
        self.max_position = sum(image.get_width() for image in self.bg_images)

    def update(self):
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            self.__scroll_left()
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            self.__scroll_right()

    def draw(self):
        self.screen.blit(self.bg_images[0], (self.current_position, 0))

    def __scroll_left(self):
        logger.debug("Scrolling LEFT.")
        self.current_position += BG_SCROLL_SPEED
        self.__update_position()

    def __scroll_right(self):
        logger.debug("Scrolling RIGHT.")
        self.current_position -= BG_SCROLL_SPEED
        self.__update_position()

    def __update_position(self):
        pass
