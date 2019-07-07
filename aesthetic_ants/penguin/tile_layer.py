import pyglet

from math import floor
from pyglet.graphics import Batch

from .constants import CollisionType, TileType
from .object import Object
from .resources import WATER_TILE, ICE_TILE, WEAK_ICE_TILE, WALL_TILE

TILE_SIZE = 16  # tile size in pixels


TILE_SERIALIZATION_MAP = {
    "W": TileType.WALL,
    "I": TileType.ICE,
    "E": TileType.WEAK_ICE,
    "A": TileType.WATER
}


class Tile(pyglet.sprite.Sprite):
    """
    Represents an individual tile in a tiled layer
    """
    def __init__(self, tile: TileType, *args, **kwargs):
        self.tile_type = tile
        super().__init__(*args, **kwargs)


class TileLayer(Object):
    """
    A class that manages a large array of tile sprites
    """
    collision_type = CollisionType.TILE_LAYER

    def __init__(self, x: int, y: int):
        self.tile_images = {
            TileType.WATER: WATER_TILE,
            TileType.ICE: ICE_TILE,
            TileType.WEAK_ICE: WEAK_ICE_TILE,
            TileType.WALL: WALL_TILE
        }

        self.x = x
        self.y = y

        self.batch = Batch()

        # Tiles is in the format [y][x]
        self.tiles = []

    def set_tile(self, tile_x: int, tile_y: int, tile_type: TileType):
        """
        Creates a new tile at a given position in the tile grid
        """
        if self.tiles[tile_y][tile_x]:
            self.tiles[tile_y][tile_x].batch = None
            self.tiles[tile_y][tile_x].delete()

        self.tiles[tile_y][tile_x] = Tile(tile_type,
                                          self.tile_images[tile_type],
                                          x=tile_x * TILE_SIZE + self.x,
                                          y=tile_y * TILE_SIZE + self.y,
                                          batch=self.batch)

    def update(self, dt, **kwargs):
        pass

    def draw(self):
        self.batch.draw()

    def erase_tiles(self):
        """Resets the tile map by disconnecting sprites from the batch"""
        for row in self.tiles:
            for tile in row:
                tile.batch = None
                tile.delete()
        self.tiles = []

    def load_tiles(self, tile_filename: str):
        """Loads a tile map from a level file"""
        with open(tile_filename, 'r') as level_file:
            level_data = level_file.readlines()
            self.erase_tiles()

            for y, line in enumerate(level_data):
                row = []
                for x, serialized_tile in enumerate(line.strip()):
                    tile_type = TILE_SERIALIZATION_MAP[serialized_tile]
                    tile = Tile(tile_type,
                                self.tile_images[tile_type],
                                x=x * TILE_SIZE + self.x,
                                y=y * TILE_SIZE + self.y,
                                batch=self.batch)
                    row.append(tile)
                self.tiles.append(row)

    def collide_tiles(self, other, _):
        """Determine which tiles collide with the passed object,
        and call collide_tile for each"""
        # Calculate the width and height in tiles of the object
        tile_width = floor(other.width * other.collision_leniency / TILE_SIZE)
        tile_height = floor(other.height * other.collision_leniency / TILE_SIZE)

        # Calculates the tile position of the object
        tile_position = ((other.x - self.x) / TILE_SIZE,
                         (other.y - self.y) / TILE_SIZE)

        # Use the tile position as a base, making a small list of tile coordinates
        # that collide with the object
        tiles = [(floor(x + tile_position[0]), floor(y + tile_position[1]))
                 for x in range(tile_width)
                 for y in range(tile_height)]

        grid_width = len(self.tiles[0])
        grid_height = len(self.tiles)
        for x, y in tiles:
            # Check if coordinates are valid
            if y < 0 or y >= grid_height:
                continue
            if x < 0 or x >= grid_width:
                continue

            other.collide_tile(self.tiles[y][x])
