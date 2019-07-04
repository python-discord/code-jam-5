import logging
import random
from typing import Any, List, Tuple

import pygame as pg
from pygame.image import load

from project.constants import (
    BG_CLOUDS_SCROLL_SPEED,
    BG_SCROLL_SPEED,
    BIOME_WIDTH,
    CLOUD_LAYERS_BG,
    CLOUD_LAYERS_FG,
    FG_CLOUDS_SCROLL_SPEED,
    HEIGHT,
    INDICATOR_ARROW,
    TILE_COLS,
    TILE_ROWS,
    TILE_WIDTH,
    WIDTH,
)
from .biome import Biome
from .game_state import GameState
from .indicator import Indicator
from .sun import Sun
from .tile import Tile


logger = logging.getLogger(__name__)
game_vars = GameState()


class Earth(object):
    """
    Represent Earth class object.

    Includes logic for handling background and game tasks.
    """

    # :: Clouds
    # pools - preloaded pool of images to choose from
    cloud_layers_bg_pool: List[pg.Surface]
    cloud_layers_bg: List[pg.Surface]
    current_cloud_bg_pos: float = 0

    cloud_layers_fg_pool: List[pg.Surface]
    cloud_layers_fg: List[pg.Surface]
    current_cloud_fg_pos: float = 0

    # :: Indicators
    indicators: List[Indicator]
    indicator_image: pg.Surface

    # :: Other
    current_biome_pos: float = 0
    biomes: List[Biome]
    max_position: float

    visible_tiles: List[Tile]

    def __init__(self, screen: pg.Surface, biomes: List[Biome]):
        self.screen = screen

        self.biomes = biomes

        self.cloud_layers_bg_pool = [
            load(str(image)).convert_alpha() for image in CLOUD_LAYERS_BG
        ]
        self.cloud_layers_bg = []
        self.cloud_layers_fg_pool = [
            load(str(image)).convert_alpha() for image in CLOUD_LAYERS_FG
        ]
        self.cloud_layers_fg = []

        self.indicator_image = load(str(INDICATOR_ARROW)).convert_alpha()

        self.indicators = []
        self.visible_tiles = []

        # Calculate max position by added the width of all bg images
        self.max_position = sum(biome.background.get_width() for biome in self.biomes)

    def update(self, event: pg.event) -> None:
        """Update game logic with each game tick."""
        if not game_vars.open_task:
            key_pressed = pg.key.get_pressed()

            if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
                self.__scroll_left()
            if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
                self.__scroll_right()

            self.__update_tiles(event)

        self.current_cloud_bg_pos += BG_CLOUDS_SCROLL_SPEED
        self.current_cloud_fg_pos += FG_CLOUDS_SCROLL_SPEED

        self.__update_positions()
        self.__update_indicators()

        open_task = game_vars.open_task
        if open_task:
            open_task.update(event)

    def draw(self, sun: Sun) -> None:
        """Draw all images related to the earth."""
        self.__draw_clouds()
        self.__draw_biomes()
        sun.draw()  # Need to draw sun before indicators
        self.__draw_indicators()

        open_task = game_vars.open_task
        if open_task:
            open_task.draw()

    def fix_indicators(self) -> None:
        """Will add missing indicators. Should be called when indicator could appear."""
        # Loop through all tiles. If tile has task, but no indicator - add it
        for biome_idx, biome in enumerate(self.biomes):
            for tile_row in biome.tilemap:
                for tile in tile_row:
                    if tile.task is None:
                        continue

                    indicator = next(
                        (i for i in self.indicators if i.tile == tile), None
                    )

                    # If tile is visible - dont need indicator
                    if tile in self.visible_tiles:
                        if indicator:
                            self.indicators.remove(indicator)
                        continue

                    if indicator is None:
                        indicator = Indicator(self.screen, tile, self.indicator_image)
                        self.indicators.append(indicator)

                    # Calculate if the tile is to the left or right of the screen
                    biome_pos = biome_idx * BIOME_WIDTH
                    if self.current_biome_pos < biome_pos:
                        distance_left = (
                            self.max_position - biome_pos + self.current_biome_pos
                        )
                        distance_right = biome_pos - self.current_biome_pos
                    else:
                        distance_left = self.current_biome_pos - biome_pos
                        distance_right = (
                            self.max_position - self.current_biome_pos + biome_pos
                        )
                    indicator.flip(distance_left <= distance_right)

    def __prepare_draw_clouds(
        self,
        pool: List[pg.Surface],
        current_list: List[pg.Surface],
        x_pos: int,
        y_pos: int = 0,
    ) -> List[Any]:
        """
        Logic to handle drawing a single cloud plane.

        Returns a list of Surface draw arguments to draw later.
        """
        draw_args = []
        offset = x_pos

        for i, cloud in enumerate(current_list):
            draw_args.append([cloud, (offset, y_pos)])
            offset += cloud.get_width()

            # Remove clouds that are offscreen to the right
            if offset > WIDTH:
                current_list = current_list[:i]
                break

        # Add new clouds to fill the rest of the screen
        while offset < WIDTH:
            new_cloud = random.choice(pool)
            current_list.append(new_cloud)
            draw_args.append([new_cloud, (offset, y_pos)])
            offset += new_cloud.get_width()

        return draw_args

    def __draw_clouds(self) -> None:
        draw_bg_args = self.__prepare_draw_clouds(
            self.cloud_layers_bg_pool,
            self.cloud_layers_bg,
            self.current_cloud_bg_pos,
            int(HEIGHT // 4),
        )
        self.screen.blits(draw_bg_args)

        draw_fg_args = self.__prepare_draw_clouds(
            self.cloud_layers_fg_pool,
            self.cloud_layers_fg,
            self.current_cloud_fg_pos,
            int(HEIGHT // 3),
        )
        self.screen.blits(draw_fg_args)

    def __prepare_draw_background(self, biome: Biome, biome_x: int) -> List[List[Any]]:
        """Returns list of parameters lists how to draw biome background."""
        return [[biome.background, (biome_x, HEIGHT - biome.background.get_height())]]

    def __prepare_draw_tiles(self, biome: Biome, biome_x: int) -> List[List[Any]]:
        """Returns list of parameters lists how to draw biomes tiles."""
        draw_args = []

        tile_y = HEIGHT - int((TILE_WIDTH * len(biome.tilemap)) // 1.5)

        for y, tiles_row in enumerate(biome.tilemap):
            # Every second row needs x offset to fit isometric tiles
            offset = int(TILE_WIDTH // 2)

            tile_x = offset if y % 2 != 0 else 0
            for tile in tiles_row:
                tile_image = tile.image
                # Horizontally centered in it's possition
                draw_x = biome_x + tile_x - (tile_image.get_width() - TILE_WIDTH) // 2
                # Vertical align to bottom - will expand upwards
                draw_y = tile_y - (tile_image.get_height() - TILE_WIDTH)
                tile.pos_x = draw_x
                tile.pos_y = draw_y
                draw_args.append([tile_image, (draw_x, draw_y)])
                tile_x += TILE_WIDTH

                # If tile is on screen add it to visible tiles list
                if draw_x + tile_image.get_width() > 0 and draw_x < WIDTH:
                    self.visible_tiles.append(tile)

            tile_y += offset

        return draw_args

    def __prepare_draw_biome(
        self, biome: Biome, biome_x: int
    ) -> Tuple[List[List[Any]], List[List[Any]]]:
        """
        Logic to handle drawing a single biome and its related objects.

        Returns a tuple of background and tile draw arguments lists to draw later.
        """
        # Background
        draw_bg_args = self.__prepare_draw_background(biome, biome_x)
        # Tiles
        draw_tile_args = self.__prepare_draw_tiles(biome, biome_x)

        return draw_bg_args, draw_tile_args

    def __draw_biomes(self) -> None:
        """Draw biomes related images - will draw as little as possible to fill the screen."""
        self.visible_tiles = []
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

        self.screen.blits(background_draws)

        # Need to draw one row at a time, between all biomes to avoid isometric tile clipping
        # Because the initial map is grouped by biomes, we need to do some magic to group by rows
        new_tile_draws = []
        for y in range(TILE_ROWS):
            for x in range(TILE_COLS - 1):
                start = TILE_COLS * TILE_ROWS * x + TILE_COLS * y
                end = start + TILE_COLS
                new_tile_draws += tile_draws[start:end]
        self.screen.blits(new_tile_draws)

    def __find_first_biome(self) -> Tuple[int, float]:
        """
        Function returns index, and position of first biome that should be drawn on the left.

        Screen and individual images widths are taken into account when finding the first biome.
        """
        _position = 0
        i = 0
        while i < len(self.biomes):
            image = self.biomes[i].background

            if _position - self.current_biome_pos + image.get_width() > 0:
                break

            _position += image.get_width()
            i += 1

        return (i, _position - self.current_biome_pos)

    def __draw_indicators(self) -> None:
        for indicator in self.indicators:
            indicator.draw()

    def __scroll_left(self) -> None:
        self.current_biome_pos -= BG_SCROLL_SPEED
        self.current_cloud_bg_pos += BG_CLOUDS_SCROLL_SPEED
        self.current_cloud_fg_pos += FG_CLOUDS_SCROLL_SPEED
        self.fix_indicators()

    def __scroll_right(self) -> None:
        self.current_biome_pos += BG_SCROLL_SPEED
        self.current_cloud_bg_pos -= BG_CLOUDS_SCROLL_SPEED * 2
        self.current_cloud_fg_pos -= FG_CLOUDS_SCROLL_SPEED * 2
        self.fix_indicators()

    def __update_positions(self) -> None:
        """Correct current position based on min and max values."""
        if self.current_biome_pos > self.max_position:
            self.current_biome_pos = 0
        elif self.current_biome_pos < 0:
            self.current_biome_pos = self.max_position

        # Cloud position will always be the position of first cloud (offscreen to the left)
        if self.current_cloud_bg_pos > 0:
            self.cloud_layers_bg = [
                random.choice(self.cloud_layers_bg_pool)
            ] + self.cloud_layers_bg
            self.current_cloud_bg_pos = -self.cloud_layers_bg[0].get_width()
        if self.current_cloud_fg_pos > 0:
            self.cloud_layers_fg = [
                random.choice(self.cloud_layers_fg_pool)
            ] + self.cloud_layers_fg
            self.current_cloud_fg_pos = -self.cloud_layers_fg[0].get_width()

    def __update_tiles(self, event: pg.event) -> None:
        """Calls update method of every tile in the game."""
        for biome in self.biomes:
            for tile_row in biome.tilemap:
                for tile in tile_row:
                    tile.update(event)

    def __update_indicators(self) -> None:
        """Calls update method of every indicator."""
        for indicator in self.indicators:
            indicator.update()
