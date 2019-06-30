import logging
from typing import List

import pygame as pg

from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains
from .earth import Earth


logger = logging.getLogger(__name__)


class Period(object):
    """
    This class represents an abstract Time Period Style.

    Game difficulties are split into Time Periods - with each time period having different
      tile styles, tasks, images and chances to spawn cities.
    """

    # List of biomes, that will be looped through
    biomes: List[Biome]

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.biomes = [
            BiomeDesert(),
            BiomeDesert(),
            BiomeDesert(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeForest(),
            BiomeForest(),
            BiomeForest(),
            BiomeCity(),
            BiomeCity(),
            BiomeCity(),
        ]

        self.earth = Earth(self.screen, self.biomes)

    def update(self) -> None:
        """Update gets called every game tick."""
        self.earth.update()

    def draw(self) -> None:
        """Draw gets called every game tick."""
        self.earth.draw()


class PeriodMedieval(Period):
    """Medieval themed Time Period."""

    pass


class PeriodModern(Period):
    """Modern time themed Time Period."""

    pass


class PeriodFuture(Period):
    """Future time themed Time Period."""

    pass
