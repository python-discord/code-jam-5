import logging
import random
from typing import List, Optional

import pygame as pg

from project.constants import TILE_COLS, TILE_ROWS
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

    time_of_last_task_spawn: Optional[int] = None
    # How many game ticks between task spawns (will be floored and converted to int)
    task_spawn_freq: float = 600
    # How much to increase task spawn frequency with each game tick
    task_spawn_freq_inc: float = 0.05

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
        self.__handle_task_spawn()

    def draw(self) -> None:
        """Draw gets called every game tick."""
        self.earth.draw()

    def __handle_task_spawn(self) -> None:
        if (
            self.time_of_last_task_spawn is None
            or self.time_of_last_task_spawn >= self.task_spawn_freq
        ):
            self.time_of_last_task_spawn = 0
            for _ in range(10):
                self.__spawn_task()
        else:
            self.time_of_last_task_spawn += 1
        self.task_spawn_freq = max(self.task_spawn_freq + self.task_spawn_freq_inc, 0)

    def __spawn_task(self) -> None:
        """Spawns a task on a random tile."""
        # TODO :: add check if tile already has a task or not

        # Get number of tiles between all biomes
        tile_count = TILE_COLS * TILE_ROWS * len(self.biomes)
        # Chose a random tile out of all
        random_tile_idx = random.randint(0, tile_count - 1)
        # Calculate biome index from the global tile index
        biome_idx = random_tile_idx // (TILE_COLS * TILE_ROWS)
        # Calculate tile index local to the biome chosen
        tile_in_biome_idx = random_tile_idx - (TILE_COLS * TILE_ROWS * biome_idx)
        tile_y = tile_in_biome_idx // TILE_COLS
        tile_x = tile_in_biome_idx - (tile_y * TILE_COLS)

        self.biomes[biome_idx].tilemap[tile_y][tile_x].has_task = True


class PeriodMedieval(Period):
    """Medieval themed Time Period."""

    pass


class PeriodModern(Period):
    """Modern time themed Time Period."""

    pass


class PeriodFuture(Period):
    """Future time themed Time Period."""

    pass
