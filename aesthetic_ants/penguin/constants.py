from enum import Enum, auto


class CollisionType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    SNOWBALL = auto()
    TILE_LAYER = auto()


class TileType(Enum):
    WATER = auto()
    WEAK_ICE = auto()
    ICE = auto()
    WALL = auto()
