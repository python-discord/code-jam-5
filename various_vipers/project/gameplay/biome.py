import logging
import random
from typing import Generator, List

import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import (
    BIOME_WIDTH,
    GAME_BG_DESERT,
    GAME_BG_FALL,
    GAME_BG_FOREST,
    GAME_BG_GRASS,
    TILES_GRASS,
    TILE_COLS,
    TILE_ROWS,
)
from .tile import Tile


logger = logging.getLogger(__name__)


class Biome(object):
    """Abstract Biome class for all biome relevant information."""

    # List of background images for this biome.
    # One will be chosen randomly to be displayed.
    background_images: List[str] = []

    other_tiles: List[str] = TILES_GRASS

    # Unique to theme tiles list
    unique_tiles: List[str] = []
    unique_tiles_chance: float = 0.3

    # Tiles that belong to cities
    city_tiles: List[str] = []
    city_tiles_chance: float = 0.2

    # Tiles that have water sources
    water_tiles: List[str] = []
    water_tiles_chance: float = 0.2

    # -----------------------
    # Current values

    # Current tilemap for this biome
    tilemap: List[List[Tile]] = []
    # Current background
    background: pg.image = None

    def __init__(self):
        self.tilemap = self.__generate_tilemap(TILE_COLS, TILE_ROWS)

        # scale background to 0.8 of screen height
        self.background = load(str(random.choice(self.background_images)))
        self.background = scale(self.background, (BIOME_WIDTH, BIOME_WIDTH))

    def __choose_tiles(self, k: int = 1) -> Generator[Tile, None, None]:
        """Returns k number of random tiles based on set tile sprites and weights to spawn."""
        other_tiles_chance = max(
            1
            - self.water_tiles_chance
            + self.city_tiles_chance
            + self.unique_tiles_chance,
            0,
        )

        # Group all tiles lists with their chances to spawn
        tiles_lists = [
            (self.other_tiles, other_tiles_chance),
            (self.unique_tiles, self.unique_tiles_chance),
            (self.city_tiles, self.city_tiles_chance),
            (self.water_tiles, self.water_tiles_chance),
        ]
        # Remove empty lists
        tiles_lists = [l for l in tiles_lists if len(l[0]) > 0]

        # k number of non-empty styled tiles
        chosen_tile_lists = random.choices(
            [l[0] for l in tiles_lists], weights=[l[1] for l in tiles_lists], k=k
        )

        for tile_list in chosen_tile_lists:
            yield Tile(str(random.choice(tile_list)))

    def __generate_tilemap(self, width: int = 10, height: int = 4) -> List[List[Tile]]:
        tilemap = []
        for _ in range(height):
            tilemap.append(list(self.__choose_tiles(width)))
        return tilemap


class BiomeDesert(Biome):
    """
    Desert themed biome.

    Desert theme biomes have a lower chance to spawn a city or water tiles.
    """

    background_images: List[str] = [GAME_BG_DESERT]

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.6,
        city_chance: float = 0.05,
        water_chance: float = 0.05,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeFall(Biome):
    """Fall themed biome."""

    background_images: List[str] = [GAME_BG_FALL]

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.6,
        city_chance: float = 0.2,
        water_chance: float = 0.1,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeForest(Biome):
    """Foresty biome."""

    background_images: List[str] = [GAME_BG_FOREST]

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.6,
        city_chance: float = 0.2,
        water_chance: float = 0.1,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeGrass(Biome):
    """Grassy biome."""

    background_images: List[str] = [GAME_BG_GRASS]

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.3,
        city_chance: float = 0.4,
        water_chance: float = 0.1,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()
