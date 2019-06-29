import logging

import pygame as pg


logger = logging.getLogger(__name__)


class GameView:
    """GameView hold the information about all things related to the main game."""

    def __init__(self):
        pass

    def update(self):
        """
        Update is called every game tick.

        Function handles basic gameplay elements and inputs.
        """
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            logger.debug("Scrolling LEFT.")
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            logger.debug("Scrolling RIGHT.")
