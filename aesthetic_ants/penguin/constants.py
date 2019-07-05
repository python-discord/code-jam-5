from enum import Enum, auto


class CollisionType(Enum):
    PLAYER = auto()
    ENEMY = auto()

    # Projectiles
    SNOWBALL = auto()
    ROCKET = auto()
    SNOWSPLOSION = auto()
