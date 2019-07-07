import logging
import random
from pathlib import PurePath
from typing import Callable, Generator, List, Tuple

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
from project.utils.helpers import load_img
from .task import Task
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
        self.tilemap = self.Tilemap(self, TILE_COLS, TILE_ROWS)

        # scale background to 0.8 of screen height
        self.background = load_img(random.choice(self.background_images))
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

    class Tilemap:
        """Tilemap class holds a 2D array of tiles for the biome."""

        def __init__(self, biome: "Biome", width: int = 10, height: int = 4):
            self.biome = biome

            self._task_coords = []  # List of tuples (y, x) for which tiles has a task
            self._tiles = []
            for _ in range(height):
                self._tiles.append(list(self.__choose_tiles(width)))

        @property
        def rows(self) -> Generator[Tile, None, None]:
            """Get rows of this tilemap."""
            for row in self._tiles:
                yield row

        @property
        def tiles_with_task(self) -> Generator[Tile, None, None]:
            """Get tiles from this biome that have a task."""
            for y, x in self._task_coords:
                yield self._tiles[y][x]

        @property
        def tasks(self) -> Generator[Task, None, None]:
            """Get tasks from this biome."""
            for tile in self.tiles_with_task:
                yield tile.task

        @property
        def task_count(self) -> int:
            """Get task count in this biome."""
            return len(self._task_coords)

        def set_task_by_coords(self, y: int, x: int, task: Task) -> None:
            """Add a task to tile in this biome. Find tile by coordinates."""
            self._task_coords.append((y, x))
            self._tiles[y][x].task = task
            logger.debug("set task")

        def set_task_by_tile(self, tile: Tile, task: Task) -> None:
            """Add a task to tile in this biome."""
            for y, row in enumerate(self._tiles):
                for x, row_tile in enumerate(row):
                    if tile == row_tile:
                        self.set_task_by_coords(y, x, task)
                        return

        def del_task_by_coords(self, y: int, x: int) -> None:
            """Remove a task from the tile in this biome. Find tile by coordintes."""
            self._task_coords.remove((y, x))
            del self._tiles[y][x].task
            logger.debug("del task")

        def del_task_by_tile(self, tile: Tile) -> None:
            """Remove a task from the tile in this biome."""
            for y, row in enumerate(self._tiles):
                for x, row_tile in enumerate(row):
                    if tile == row_tile:
                        self.del_task_by_coords(y, x)
                        return

        def __iter__(self):
            """Iterate through tiles in this biome."""
            return iter(self._tiles)

        def __getitem__(self, key: int):
            """Get a tile from this biome."""
            return self._tiles[key]

        def __len__(self):
            """Get length (rows) of tiles in this biome."""
            return len(self._tiles)

        def __choose_tiles(self, k: int = 1) -> Generator[Tile, None, None]:
            """Returns k number of random tiles themed on biome and weights to spawn."""
            other_tiles_chance = max(
                1
                - self.biome.water_tiles_chance
                + self.biome.city_tiles_chance
                + self.biome.unique_tiles_chance,
                0,
            )

            # Group all tiles lists with their chances to spawn
            tiles_lists = [
                (self.biome.other_tiles, other_tiles_chance),
                (self.biome.unique_tiles, self.biome.unique_tiles_chance),
                (self.biome.city_tiles, self.biome.city_tiles_chance),
                (self.biome.water_tiles, self.biome.water_tiles_chance),
            ]
            # Remove empty lists
            tiles_lists = [l for l in tiles_lists if len(l[0]) > 0]

            # k number of non-empty styled tiles
            chosen_tile_lists = random.choices(
                [l[0] for l in tiles_lists], weights=[l[1] for l in tiles_lists], k=k
            )

            for tile_list in chosen_tile_lists:
                yield Tile(str(random.choice(tile_list)))


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
