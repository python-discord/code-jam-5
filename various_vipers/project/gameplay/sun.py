import logging
from typing import List

import pygame as pg

from project.constants import HEIGHT, MAX_HEAT, SUN_IMAGE, WIDTH
from .biome import Biome


logger = logging.getLogger(__name__)


class Sun:
    """Class holds information about sun, its state and current heat."""

    background_image: pg.Surface = SUN_IMAGE
    current_heat: float = 0
    angle: float = 0
    min_angle_vel: float = 0.5
    max_angle_vel: float = 4

    def __init__(self, screen: pg.Surface, biomes: List[Biome], heat_per_task: float):
        self.screen = screen

        self.biomes = biomes
        self.heat_per_sec = heat_per_task

        self.image = pg.image.load(str(self.background_image)).convert_alpha()
        new_height = int(HEIGHT // 2)
        scale_percent = new_height / self.image.get_height()
        new_width = int(self.image.get_width() * scale_percent)
        self.image = pg.transform.scale(self.image, (new_width, new_height))

    def update(self) -> None:
        """Update is called every game tick."""
        self.update_angle()

        # Increase heat based on uncompleted task count
        task_count = 0
        # Get uncompleted task count. weeeee
        for biome in self.biomes:
            for row in biome.tilemap:
                for tile in row:
                    if tile.task:
                        task_count += 1
        self.current_heat += self.heat_per_sec * task_count

    def update_angle(self) -> None:
        """Update suns angle relative to itself. Called every game tick."""
        # Calculate angular velocity based on current heat
        heat_range = self.current_heat / MAX_HEAT
        velocity_range = self.max_angle_vel - self.min_angle_vel
        angle_velocity = heat_range * velocity_range + self.min_angle_vel
        # You spin me right round
        self.angle += angle_velocity
        if self.angle >= 360:
            self.angle = self.angle - 360

    def draw(self) -> None:
        """Draw is called every game tick."""
        self.screen.blit(
            pg.transform.rotate(self.image, self.angle),
            self.image.get_rect(center=(0, 0)),
        )

        # Draw current heat number
        font = pg.font.Font(None, 50)
        text = f"{str(int(self.current_heat))} / {str(MAX_HEAT)}"
        heat_indicator = font.render(text, True, pg.Color("black"))
        self.screen.blit(
            heat_indicator, (int(WIDTH // 2) - int(heat_indicator.get_width() // 2), 40)
        )
