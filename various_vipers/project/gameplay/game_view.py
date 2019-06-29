import logging
from typing import List

import pygame as pg

from .period import PeriodFuture, PeriodMedieval, PeriodModern


logger = logging.getLogger(__name__)


class GameView:
    """GameView hold the information about all things related to the main game."""

    # Background images that will be looping
    BG_images: List[str] = []

    def __init__(self, screen: pg.Surface, difficulty: int = 0):
        """
        Initializer for GameView class.

        screen - parent screen to draw objects on
        difficulty - 0, 1, 2. Difficulty increases with number.
        """
        self.screen = screen

        if difficulty == 0:
            self.period = PeriodMedieval(self.screen)
        elif difficulty == 1:
            self.period = PeriodModern(self.screen)
        elif difficulty == 2:
            self.period = PeriodFuture(self.screen)
        else:
            raise TypeError(f"Unknown difficulty level passed: {difficulty}")

    def update(self) -> None:
        """Update gets called every game tick."""
        self.period.update()

    def draw(self) -> None:
        """Draw gets called every game tick."""
        self.period.draw()
