import pyglet
import random

from .constants import CollisionType
from .object import PhysicalObject
from .resources import ENEMY_IMAGE


class Enemy(PhysicalObject):
    collision_type = CollisionType.ENEMY

    def __init__(self):
        super().__init__(ENEMY_IMAGE)

        self.velocity_x = random.randint(0, 100)
        self.velocity_y = random.randint(0, 100)

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
