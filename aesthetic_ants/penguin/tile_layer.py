import itertools
import pyglet
import random

from math import floor
from pyglet.graphics import Batch
from typing import List

from .constants import CollisionType, TileType
from .enemy import Enemy
from .object import Object
from .resources import WATER_TILE, ICE_TILE, WEAK_ICE_TILE, WALL_TILE

# Tile size in pixels
TILE_SIZE = 16

# Ticks until a decayable tile decays
ICE_HEALTH = 25
WEAK_ICE_HEALTH = 35

# Base decay rate, per second
DECAY_RATE = 30

# How much enemy number should weight the decay
# Each enemy adds this much to DECAY_RATE while it is alive
ENEMY_DECAY_INFLUENCE = 5

# How much nearby weak tiles should weight the decay
# Each weak tile within NEARBY_TILES adds this to the decay rate
WEAK_TILE_DECAY_INFLUENCE = 1.5

# How much health is lost each "tick" of a tile, random within the range
DECAY_VARIANCE = (0, 1)

# Precomputed "nearby tiles" that influence tile decay
NEARBY_TILES = list(itertools.product([-1, 0, 1], [-1, 0, 1]))


# Maps tiles from their level-file character to tile type
TILE_SERIALIZATION_MAP = {
    "W": TileType.WALL,
    "I": TileType.ICE,
    "E": TileType.WEAK_ICE,
    "A": TileType.WATER
}


# Maps decayable tiles to their descendant tile type
DECAY_MAP = {
    TileType.ICE: TileType.WEAK_ICE,
    TileType.WEAK_ICE: TileType.WATER
}

# Tiles that are weak enough that nearby tiles decay faster
WEAK_TILES = {TileType.WEAK_ICE, TileType.WATER}


class Tile(pyglet.sprite.Sprite):
    """
    Represents an individual tile in a tiled layer
    """
    def __init__(self, tile: TileType, *args, health=0, **kwargs):
        self.tile_type = tile

        if not health:
            if self.tile_type == TileType.ICE:
                self.health = random.random() * ICE_HEALTH
            elif self.tile_type == TileType.WEAK_ICE:
                self.health = random.random() * WEAK_ICE_HEALTH
            else:
                self.health = -1
        else:
            self.health = health

        super().__init__(*args, **kwargs)


class TileLayer(Object):
    """
    A class that manages a large array of tile sprites
    """
    collision_type = CollisionType.TILE_LAYER
    decay = 0

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

    def update(self, dt: float, **kwargs):
        enemies = list(filter(lambda obj: isinstance(obj, Enemy),
                              self.space.objects))
        self.decay_tiles(dt, enemies)

    def draw(self):
        self.batch.draw()

    def erase_tiles(self):
        """Resets the tile map by disconnecting sprites from the batch"""
        for row in self.tiles:
            for tile in row:
                tile.batch = None
                tile.delete()
        self.tiles = []

    def load_tiles(self, level):
        """Loads a tile map from a level file"""
        level_data = level.text.split("\n")
        self.erase_tiles()

        for y, line in enumerate(level_data):
            row = []
            for x, serialized_tile in enumerate(line):
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
            if not 0 <= y < grid_height:
                continue
            if not 0 <= x < grid_width:
                continue

            other.collide_tile(self.tiles[y][x])

    def decay_tiles(self, dt: float, enemies: List[Enemy]):
        self.decay += DECAY_RATE * dt
        self.decay += dt * ENEMY_DECAY_INFLUENCE * len(enemies)

        grid_width = len(self.tiles[0])
        grid_height = len(self.tiles)

        for _ in range(round(self.decay)):
            self.decay -= 1
            x = random.randrange(grid_width)
            y = random.randrange(grid_height)
            tile = self.tiles[y][x]
            if tile.tile_type in DECAY_MAP:
                tile_weakness = 0
                for offset_x, offset_y in NEARBY_TILES:
                    # Skip out of bounds tiles
                    if not 0 <= x + offset_x < grid_width:
                        continue
                    if not 0 <= y + offset_y < grid_height:
                        continue

                    if self.tiles[y + offset_y][x + offset_x].tile_type in WEAK_TILES:
                        tile_weakness += WEAK_TILE_DECAY_INFLUENCE

                tile.health -= DECAY_VARIANCE[0] \
                    + random.random() * DECAY_VARIANCE[1] \
                    + tile_weakness

                if tile.health < 0:
                    self.set_tile(x, y, DECAY_MAP[tile.tile_type])
