import logging

import pygame as pg
from pygame.image import load


logger = logging.getLogger(__name__)


class Earth(object):
    current_position = 0

    def __init__(self, screen, bg_images, tilemap):
        self.screen = screen
        self.bg_images = bg_images
        self.tilemap = tilemap

    def update(self):
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            logger.debug("Scrolling LEFT.")
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            logger.debug("Scrolling RIGHT.")

    def draw(self):
        self.screen.blit(load(str(self.bg_images[self.current_position])), (0, 0))
