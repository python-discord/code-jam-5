import logging
from typing import List

import pygame as pg

from project.constants import HEIGHT, MAX_HEAT, SUN_IMAGE, THERMO, THERMO_FILL, WIDTH
from .biome import Biome
from .game_state import GameState


logger = logging.getLogger(__name__)
game_vars = GameState()


class Sun:
    """Class holds information about sun, its state and current heat."""

    angle: float = 0
    min_angle_vel: float = 0.5
    max_angle_vel: float = 4

    def __init__(
        self,
        screen: pg.Surface,
        biomes: List[Biome],
        heat_per_tick: float,
        heat_per_task: float,
    ):
        self.screen = screen

        self.biomes = biomes
        self.heat_per_tick = heat_per_tick
        self.heat_per_task = heat_per_task

        self.thermo = pg.image.load(str(THERMO)).convert_alpha()
        self.thermo_fill = pg.image.load(str(THERMO_FILL)).convert_alpha()

        # Sun image
        self.image = pg.image.load(str(SUN_IMAGE)).convert_alpha()
        new_height = int(HEIGHT // 2)
        scale_percent = new_height / self.image.get_height()
        new_width = int(self.image.get_width() * scale_percent)
        self.image = pg.transform.scale(self.image, (new_width, new_height))
        # Create cache of every image rotation, so we don't have to calculate each time
        self._image_cache = []
        for angle in range(361):
            self._image_cache.append(pg.transform.rotate(self.image, angle))

    def update(self, event: pg.event) -> None:
        """Update is called every game tick."""
        self.update_angle()

        if game_vars.is_started:
            # Increase heat based on uncompleted task count
            task_count = 0
            # Get uncompleted task count. weeeee
            for biome in self.biomes:
                for row in biome.tilemap:
                    for tile in row:
                        if tile.task:
                            task_count += 1

            game_vars.current_heat += (
                self.heat_per_tick + self.heat_per_task * task_count
            )
            game_vars.current_heat = min(max(game_vars.current_heat, 0), MAX_HEAT)

    def draw(self) -> None:
        """Draw is called every game tick."""
        self.screen.blit(
            self._image_cache[int(self.angle)], self.image.get_rect(center=(0, 0))
        )

        if game_vars.is_started:
            percent = game_vars.current_heat / MAX_HEAT
            fill_rect = self.thermo_fill.get_rect()
            fill_rect.y = int(self.thermo_fill.get_height() * max(0.9 - percent, 0))
            self.screen.blit(self.thermo, (WIDTH - self.thermo.get_width() - 10, 10))
            self.screen.blit(
                self.thermo_fill,
                (WIDTH - self.thermo_fill.get_width() - 10, 10 + fill_rect.y),
                fill_rect,
            )

    def update_angle(self) -> None:
        """Update suns angle relative to itself. Called every game tick."""
        # Calculate angular velocity based on current heat
        heat_range = game_vars.current_heat / MAX_HEAT
        velocity_range = self.max_angle_vel - self.min_angle_vel
        angle_velocity = heat_range * velocity_range + self.min_angle_vel
        # You spin me right round
        self.angle += angle_velocity
        self.angle %= 360
