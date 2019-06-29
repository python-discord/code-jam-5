import logging
import pygame as pg

logger = logging.getLogger(__name__)


class GameView:
    def __init__(self):
        pass

    def update(self):
        """
        This function is called every game tick.
        Function handles basic gameplay elements and inputs.
        """
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a]:
            logger.debug("Pressed A key.")
        if key_pressed[pg.K_d]:
            logger.debug("Pressed D key.")
