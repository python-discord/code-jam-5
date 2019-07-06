import random

from .snowball import Snowball
from .constants import CollisionType
from .object import PhysicalObject
from .resources import ENEMY_IMAGE


class Enemy(PhysicalObject):
    collision_type = CollisionType.ENEMY
    score = 5

    def __init__(self, x, y):
        super().__init__(ENEMY_IMAGE, x=x, y=y)

        self.velocity_x = random.randint(0, 100)
        self.velocity_y = random.randint(0, 100)

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def on_collision_snowball(self, snowball: Snowball):
        self.space.remove(self)
        self.space.remove(snowball)
