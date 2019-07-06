import pyglet

from enum import Enum
from pyglet.graphics import Batch
import random

from .constants import CollisionType
from .object import Object
from .resources import WATER_TILE, ICE_TILE, WEAK_ICE_TILE, WALL_TILE

TILE_SIZE = 16  # tile size in pixels


class TileType(Enum):
    WATER_TILE = 1
    WEAK_ICE_TILE = 2
    ICE_TILE = 3
    WALL_TILE = 4


TILE_SERIALIZATION_MAP = {
    "W": TileType.WALL_TILE,
    "I": TileType.ICE_TILE,
    "E": TileType.WEAK_ICE_TILE,
    "A": TileType.WATER_TILE
}


class Tile(pyglet.sprite.Sprite):
    """
    Represents an individual tile in a tiled layer
    """
    def __init__(self, tile, *args, **kwargs):
        self.tile_type = tile
        super().__init__(*args, **kwargs)


class TileLayer(Object):
    """
    A class that manages a large array of tile sprites
    """
    collision_type = CollisionType.TILE_LAYER

    def __init__(self, width: int, height: int):
        self.tile_images = {
            TileType.WATER_TILE: WATER_TILE,
            TileType.ICE_TILE: ICE_TILE,
            TileType.WEAK_ICE_TILE: WEAK_ICE_TILE,
            TileType.WALL_TILE: WALL_TILE
        }

        self.batch = Batch()

        self.width = width
        self.height = height

        self.tile_width = width // TILE_SIZE
        self.tile_height = height // TILE_SIZE

        self.tiles = [[Tile(TileType.WATER_TILE,
                            img=self.tile_images[
                                random.choice([*self.tile_images.keys()])
                            ],
                            x=x*TILE_SIZE,
                            y=y*TILE_SIZE,
                            batch=self.batch)
                       for y in range(self.tile_height)]
                      for x in range(self.tile_width)]

    def create_tile(self, tile_x: int, tile_y: int, tile_type: TileType):
        """
        Creates a new tile at a given position in the tile grid
        """
        if self.tiles[tile_x][tile_y]:
            self.tiles[tile_x][tile_y].batch = None
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

    def add_to_space(self, space):
        super().add_to_space(space)

    def load_tiles(self, tile_filename):
        """Loads a tile map from a level file. Levels are 40x30 tiles by default"""
        with open(tile_filename, 'r') as level_file:
            level_data = level_file.readlines()
            for y, line in enumerate(level_data):
                for x, tile in enumerate(line.strip()):
                    self.create_tile(x, y, TILE_SERIALIZATION_MAP[tile])
