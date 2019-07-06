import logging
import random
from pathlib import PurePath
from typing import Callable, Generator, List, Tuple

from pygame.image import load
from pygame.transform import scale

from project.constants import (
    BIOME_WIDTH,
    CITY_BGS,
    Color,
    DESERT_BGS,
    FOREST_BGS,
    MOUNTAINS_BGS,
    TILES_GRASS,
    TILES_WATER,
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
    water_tiles: List[str] = TILES_WATER
    water_tiles_chance: float = 0.2

    # Text that shows up when task is completed successfully
    text_task_success: str = ""
    # Text that shows up when task is completed unsuccessfully
    text_task_fail: str = ""

    def __init__(self):
        self.tilemap = self.__generate_tilemap(TILE_COLS, TILE_ROWS)

        # scale background to 0.8 of screen height
        self.background = load(
            str(random.choice(self.background_images))
        ).convert_alpha()
        self.background = scale(self.background, (BIOME_WIDTH, BIOME_WIDTH))

    @property
    def color(self) -> Tuple[Color, Color]:
        """Returns color of this biome's type. [color, color for hover]."""
        if isinstance(self, BiomeCity):
            return (Color.city, Color.city_hover)
        elif isinstance(self, BiomeDesert):
            return (Color.desert, Color.desert_hover)
        elif isinstance(self, BiomeForest):
            return (Color.forest, Color.forest_hover)
        elif isinstance(self, BiomeMountains):
            return (Color.mountains, Color.mountains_hover)
        else:
            raise NameError(f"Colors not found for biome: {type(self)}")

    def image_from(self, images: Callable[[str], PurePath]) -> PurePath:
        """Get image from callable function of images that is of this biome's type."""
        if isinstance(self, BiomeCity):
            return images("city")
        elif isinstance(self, BiomeDesert):
            return images("desert")
        elif isinstance(self, BiomeForest):
            return images("forest")
        elif isinstance(self, BiomeMountains):
            return images("mountains")
        else:
            raise NameError(f"Task image not found for biome: {type(self)}")

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

    background_images: List[str] = DESERT_BGS

    unique_tiles: List[str] = []

    unique_tiles_chance: float = 0.6
    city_tiles_chance: float = 0.05
    water_tiles_chance: float = 0.05

    text_task_success: str = "Solar panels installed"
    text_task_fail: str = "Factory was built"


class BiomeCity(Biome):
    """City themed biome."""

    background_images: List[str] = CITY_BGS

    unique_tiles: List[str] = []

    unique_tiles_chance: float = 0.3
    city_tiles_chance: float = 0.5
    water_tiles_chance: float = 0.05

    text_task_success: str = "Pollution decreased"
    text_task_fail: str = "Pollution increased"


class BiomeForest(Biome):
    """Foresty biome."""

    background_images: List[str] = FOREST_BGS

    unique_tiles: List[str] = []

    unique_tiles_chance: float = 0.6
    city_tiles_chance: float = 0.2
    water_tiles_chance: float = 0.1

    text_task_success: str = "You saved the forest"
    text_task_fail: str = "The forest was destroyed"


class BiomeMountains(Biome):
    """Mountain themed biome."""

    background_images: List[str] = MOUNTAINS_BGS

    unique_tiles: List[str] = []

    unique_tiles_chance: float = 0.8
    city_tiles_chance: float = 0.1
    water_tiles_chance: float = 0.1

    text_task_success: str = "Mountains saved"
    text_task_fail: str = "Mountains not saved"
