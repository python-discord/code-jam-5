import pyglet

from enum import Enum
from pyglet.graphics import Batch

from .utils import loader


TILE_SIZE = 16  # tile size in pixels


class TileType(Enum):
    WATER_TILE = 1
    WEAK_ICE_TILE = 2
    ICE_TILE = 3
    WALL_TILE = 4


class Tile(pyglet.sprite.Sprite):
    """
    Represents an individual tile in a tiled layer
    """
    def __init__(self, tile, *args, **kwargs):
        self.tile_type = tile
        super().__init__(*args, **kwargs)


class TileLayer:
    """
    A class that manages a large array of tile sprites
    """
    def __init__(self, width: int, height: int):
        self.tile_images = {
            TileType.WATER_TILE: loader.image("tiles/water.png"),
            TileType.ICE_TILE: loader.image("tiles/ice.png"),
            TileType.WEAK_ICE_TILE: loader.image("tiles/weak_ice.png"),
            TileType.WALL_TILE: loader.image("tiles/wall.png")
        }

        self.width = width
        self.height = height

        self.tile_width = width // TILE_SIZE
        self.tile_height = height // TILE_SIZE

        self.tiles = [[None] * self.tile_height] * self.tile_width

        self.init()

        self.batch = Batch()

    def init(self):
        """
        Initializes the tileset with waters
        """
        for x, tile_row in enumerate(self.tiles):
            for y, tile in enumerate(tile_row):
                self.create_tile(x, y, TileType.WATER_TILE)

    def create_tile(self, tile_x: int, tile_y: int, tile_type: TileType):
        """
        Creates a new tile at a given position in the tile grid
        """
        if self.tiles[tile_x][tile_y]:
            del self.tiles[tile_x][tile_y].batch
            self.tiles[tile_x][tile_y].delete()

        self.tiles[tile_x][tile_y] = Tile(tile_type,
                                          self.tile_images[tile_type],
                                          x=tile_x * TILE_SIZE,
                                          y=tile_y * TILE_SIZE,
                                          batch=self.batch)

    def update(self, dt, **kwargs):
        pass

    def draw(self):
        self.batch.draw()
