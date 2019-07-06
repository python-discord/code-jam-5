from enum import Enum, auto


class CollisionType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    SNOWBALL = auto()
    TILE_LAYER = auto()


class TileType(Enum):
    WATER_TILE = auto()
    WEAK_ICE_TILE = auto()
    ICE_TILE = auto()
    WALL_TILE = auto()
