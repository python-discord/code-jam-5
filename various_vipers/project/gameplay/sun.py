import logging
from typing import List

import pygame as pg

from project.constants import HEIGHT, MAX_HEAT, SUN_IMAGE, WIDTH
from .biome import Biome
from .game_state import GameState


logger = logging.getLogger(__name__)
game_vars = GameState()


class Sun:
    """Class holds information about sun, its state and current heat."""

    background_image: pg.Surface = SUN_IMAGE
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

        self.image = pg.image.load(str(self.background_image)).convert_alpha()
        new_height = int(HEIGHT // 2)
        scale_percent = new_height / self.image.get_height()
        new_width = int(self.image.get_width() * scale_percent)
        self.image = pg.transform.scale(self.image, (new_width, new_height))
        # Create cache of every image rotation, so we don't have to calculate each time
        self._image_cache = {}
        for angle in range(361):
            self._image_cache[angle] = pg.transform.rotate(self.image, angle)

    def update(self, event: pg.event) -> None:
        """Update is called every game tick."""
        self.update_angle()

        if game_vars.is_playing:
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

        if game_vars.is_playing:
            # Draw current heat number
            font = pg.font.Font(None, 50)
            text = f"{str(int(game_vars.current_heat))} / {str(MAX_HEAT)}"
            heat_indicator = font.render(text, True, pg.Color("black"))
            # screen middle top
            text_x = int(WIDTH // 2) - int(heat_indicator.get_width() // 2)
            text_y = 40
            self.screen.blit(heat_indicator, (text_x, text_y))

    def update_angle(self) -> None:
        """Update suns angle relative to itself. Called every game tick."""
        # Calculate angular velocity based on current heat
        heat_range = game_vars.current_heat / MAX_HEAT
        velocity_range = self.max_angle_vel - self.min_angle_vel
        angle_velocity = heat_range * velocity_range + self.min_angle_vel
        # You spin me right round
        self.angle += angle_velocity
        self.angle %= 360
