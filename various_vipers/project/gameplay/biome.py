import logging
import random
from typing import Generator

from pygame.image import load

from project.constants import (
    GAME_BG_DESERT,
    GAME_BG_FALL,
    GAME_BG_FOREST,
    GAME_BG_GRASS,
)
from project.constants import TILES_GRASS
from .tile import Tile


logger = logging.getLogger(__name__)


class Biome(object):
    """Abstract Biome class for all biome relevant information."""

    # List of background images for this biome.
    # One will be chosen randomly to be displayed.
    background_images = []

    other_tiles = TILES_GRASS

    # Unique to theme tiles list
    unique_tiles = []
    unique_tiles_chance = 0.3

    # Tiles that belong to cities
    city_tiles = []
    city_tiles_chance = 0.2

    # Tiles that have water sources
    water_tiles = []
    water_tiles_chance = 0.2

    # Current tilemap for this biome
    tilemap = []

    def __init__(self):
        self.tilemap = self.__generate_tilemap(10, 4)

    def get_bg(self):
        """Returns a loaded background image (chosend randomly)."""
        return load(str(random.choice(self.background_images)))

    def get_tiles(self, k=1) -> Generator[Tile, None, None]:
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

    def __generate_tilemap(self, width=10, height=4):
        tilemap = []
        for _ in range(height):
            tilemap.append(list(self.get_tiles(width)))
        return tilemap


class BiomeDesert(Biome):
    """
    Desert themed biome.

    Desert theme biomes have a lower chance to spawn a city or water tiles.
    """

    background_images = [GAME_BG_DESERT]

    unique_tiles = []

    def __init__(self, unique_chance=0.6, city_chance=0.05, water_chance=0.05):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeFall(Biome):
    """Fall themed biome."""

    background_images = [GAME_BG_FALL]

    unique_tiles = []

    def __init__(self, unique_chance=0.6, city_chance=0.2, water_chance=0.1):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeForest(Biome):
    """Foresty biome."""

    background_images = [GAME_BG_FOREST]

    unique_tiles = []

    def __init__(self, unique_chance=0.6, city_chance=0.2, water_chance=0.1):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeGrass(Biome):
    """Grassy biome."""

    background_images = [GAME_BG_GRASS]

    unique_tiles = []

    def __init__(self, unique_chance=0.3, city_chance=0.4, water_chance=0.1):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()
