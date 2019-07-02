import logging
from typing import List

import pygame as pg

from project.constants import SUN_IMAGE, HEIGHT
from .biome import Biome


logger = logging.getLogger(__name__)


class Sun:
    """Class holds information about sun, its state and current heat."""

    background_image: pg.Surface = SUN_IMAGE
    current_heat: float = 0
    angle: float = 0

    def __init__(self, screen: pg.Surface, biomes: List[Biome], heat_per_task: float):
        self.screen = screen

        self.biomes = biomes
        self.heat_per_sec = heat_per_task

        self.image = pg.image.load(str(self.background_image)).convert_alpha()
        new_height = int(HEIGHT // 2.5)
        scale_percent = new_height / self.image.get_height()
        new_width = int(self.image.get_width() * scale_percent)
        self.image = pg.transform.scale(self.image, (new_width, new_height))

    def update(self) -> None:
        """Update is called every game tick."""
        self.angle += 1
        self.angle %= 360
        # Increase heat based on uncompleted task count
        task_count = 0
        # Get uncompleted task count. weeeee
        for biome in self.biomes:
            for row in biome.tilemap:
                for tile in row:
                    if tile.task:
                        task_count += 1
        self.current_heat -= self.heat_per_sec * task_count

    def draw(self) -> None:
        """Draw is called every game tick."""
        self.screen.blit(
            pg.transform.rotate(self.image, self.angle),
            self.image.get_rect(center=(0, 0)),
        )
