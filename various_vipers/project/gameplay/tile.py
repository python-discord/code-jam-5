from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

import pygame as pg

from project.constants import TILE_WIDTH
from project.utils.helpers import load_img
from .game_state import GameState

if TYPE_CHECKING:
    # Avoid cyclic imports
    # https://stackoverflow.com/a/39757388
    from .task import Task


logger = logging.getLogger(__name__)
game_vars = GameState()


class Tile:
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    _image: pg.Surface = None

    pos_x: int = 0
    pos_y: int = 0

    # Current task associated with this tile
    # Tiles with tasks have different appearance
    task: Optional[Task] = None
    # If currently hovering over the tile
    is_hovering: bool = False

    # Variables to handle tile transformation
    # Storing scale as x multiplier to be able to use dict key
    scale_n_max: float = 20  # How many times we can scale up
    scale_n_current: float = 1  # How many times we scaled up
    breathing_speed: float = 0.025  # how much to scale on each game tick
    breathing_direction: int = 1  # 1 -> outwards, -1 -> inwards

    def __init__(self, image: str):
        self._image = load_img(image)

        scale_percent = TILE_WIDTH / self._image.get_width()
        new_height = int(self._image.get_height() * scale_percent)

        # scale image based on game screen size
        self._image = pg.transform.scale(self._image, (TILE_WIDTH, new_height))
        # Cache every possible scale of image
        _image_width = self._image.get_width()
        _image_height = self._image.get_height()
        self._image_cache = {}
        scale_n = 1
        while scale_n <= self.scale_n_max:
            new_width = int(_image_width * (1 + scale_n * self.breathing_speed))
            new_height = int(_image_height * (1 + scale_n * self.breathing_speed))
            self._image_cache[scale_n] = pg.transform.scale(
                self._image, (new_width, new_height)
            )
            scale_n += 1

    def update(self, event: pg.event) -> None:
        """Update is called every game tick."""
        # Check if this task was completed
        if self.task is None:
            self.scale_n_current = 1

        # Mouse over
        image_size = self._image_cache[self.scale_n_current].get_size()
        tile_rect = pg.Rect(
            (self.pos_x, self.pos_y), (image_size[0], image_size[1] // 2)
        )
        if not game_vars.open_task and tile_rect.collidepoint(pg.mouse.get_pos()):
            if event.type == pg.MOUSEBUTTONDOWN and self.task is not None:
                self.task.start()
            self.is_hovering = True
        else:
            self.is_hovering = False

        # Animation
        self._breathe()

    @property
    def image(self) -> pg.Surface:
        """
        Returns image of this tile.

        Method transforms the image based on if it is a task or not.
        """
        # Get image from cache based on current scale
        transformed_image = self._image_cache[self.scale_n_current].copy()
        if self.task is not None:
            # Add colored tint
            transformed_image.fill((255, 0, 0), special_flags=pg.BLEND_MULT)
        if self.is_hovering:
            transformed_image.fill((0, 0, 255), special_flags=pg.BLEND_MULT)

        return transformed_image

    def _breathe(self) -> None:
        """Will add "breathing" effect to the tile if it has a task active."""
        if self.task is not None:
            # Limit scale
            if self.scale_n_current >= self.scale_n_max:
                self.breathing_direction = -1
            elif self.scale_n_current <= 1:
                self.breathing_direction = 1

            self.scale_n_current += 1 * self.breathing_direction
