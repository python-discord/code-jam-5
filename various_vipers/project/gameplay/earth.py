import logging
from typing import Any, List, Tuple

import pygame as pg

from project.constants import (
    BG_SCROLL_SPEED,
    HEIGHT,
    TILE_COLS,
    TILE_ROWS,
    TILE_WIDTH,
    WIDTH,
)
from .biome import Biome


logger = logging.getLogger(__name__)


class Earth(object):
    """
    Represent Earth class object.

    Includes logic for handling background and game tasks.
    """

    current_position: float = 0
    biomes: List[Biome]
    max_position: float

    def __init__(self, screen: pg.Surface, biomes: List[Biome]):
        self.screen = screen

        self.biomes = biomes

        # Calculate max position by added the width of all bg images
        self.max_position = sum(biome.background.get_width() for biome in self.biomes)

    def update(self) -> None:
        """Update game logic with each game tick."""
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            self.__scroll_left()
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            self.__scroll_right()

    def draw(self) -> None:
        """Draw all images related to the earth."""
        self.__draw_biomes()

    def __prepare_draw_biome(
        self, biome: Biome, biome_x: int
    ) -> Tuple[List[Any], List[Any]]:
        """
        Logic to handle drawing a single biome and its related objects.

        Returns a tuple of background and tile draw arguments to draw later.
        """
        draw_bg_args = []
        draw_tile_args = []

        # Draw background
        draw_bg_args.append([biome.background, (biome_x, HEIGHT // 5)])

        # Draw tiles
        tile_y = HEIGHT - int((TILE_WIDTH * len(biome.tilemap)) // 1.5)
        for y, tiles_row in enumerate(biome.tilemap):
            # Every second row needs x offset to fit isometric tiles
            offset = int(TILE_WIDTH // 2)

            tile_x = offset if y % 2 != 0 else 0
            for tile in tiles_row:
                draw_tile_args.append([tile.image, (biome_x + tile_x, tile_y)])
                tile_x += tile.image.get_width()

            tile_y += offset

        return draw_bg_args, draw_tile_args

    def __draw_biomes(self) -> None:
        """Draw biomes related images - will draw as little as possible to fill the screen."""
        # Saving draw calls to buffer and draw later - so we can draw all BG items before FG
        background_draws = []
        tile_draws = []
        # Get first biome to draw from
        i, biome_x = self.__find_first_biome()
        # From the first BG image, draw new images to the right, until whole screen is filled
        while True:
            if i > len(self.biomes) - 1:
                # Loop images
                i = 0

            biome = self.biomes[i]
            image = biome.background
            bg_draws, fg_draws = self.__prepare_draw_biome(biome, biome_x)
            background_draws += bg_draws
            tile_draws += fg_draws

            biome_x += image.get_width()
            if biome_x > WIDTH:
                break

            i += 1

        for draw in background_draws:
            self.screen.blit(*draw)

        # Need to draw one row at a time, between all biomes to avoid isometric tile clipping
        # Because the initial map is grouped by biomes, we need to do some magic to group by rows
        new_tile_draws = []
        for y in range(TILE_ROWS):
            for x in range(TILE_COLS - 1):
                start = TILE_COLS * TILE_ROWS * x + TILE_COLS * y
                end = start + TILE_COLS
                new_tile_draws += tile_draws[start:end]
        for draw in new_tile_draws:
            self.screen.blit(*draw)

    def __find_first_biome(self) -> Tuple[int, float]:
        """
        Function returns index, and position of first biome that should be drawn on the left.

        Screen and individual images widths are taken into account when finding the first biome.
        """
        _position = 0
        i = 0
        while i < len(self.biomes):
            image = self.biomes[i].background

            if _position - self.current_position + image.get_width() > 0:
                break

            _position += image.get_width()
            i += 1

        return (i, _position - self.current_position)

    def __scroll_left(self) -> None:
        logger.debug("Scrolling LEFT.")
        self.current_position -= BG_SCROLL_SPEED
        self.__update_position()

    def __scroll_right(self) -> None:
        logger.debug("Scrolling RIGHT.")
        self.current_position += BG_SCROLL_SPEED
        self.__update_position()

    def __update_position(self) -> None:
        """Correct current position based on min and max values."""
        if self.current_position > self.max_position:
            self.current_position = 0
        elif self.current_position < 0:
            self.current_position = self.max_position
