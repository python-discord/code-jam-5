import logging

import pygame as pg
from pygame.image import load

from project.constants import GAME_BG_IMAGES


logger = logging.getLogger(__name__)


class GameView:
    """GameView hold the information about all things related to the main game."""

    # Background images that will be looping
    BG_images = []

    def __init__(self, screen):
        self.screen = screen

        self.background = Background(self.screen)

    def update(self):
        """
        Update is called every game tick.

        Function handles basic gameplay elements and inputs.
        """
        self.background.update()

        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            logger.debug("Scrolling LEFT.")
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            logger.debug("Scrolling RIGHT.")


class Background:
    """
    Background class holds all information related to game background.

    Class holds - images, scroll logic, position, etc.
    """

    # List of images that will be glued together
    # Images will cycle through (after last one - first one will be used).
    images = GAME_BG_IMAGES
    # Current position
    current_position = 0

    def __init__(self, screen):
        self.screen = screen

    def update(self):
        self.screen.blit(load(str(self.images[0])), (0, 0))
