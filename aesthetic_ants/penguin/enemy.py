import random

from .snowball import Snowball
from .constants import CollisionType
from .object import Object
from .object import PhysicalObject
from .resources import ENEMY_BIG_IMAGE, ENEMY_FAST_IMAGE


class Enemy(PhysicalObject):
    collision_type = CollisionType.ENEMY
    score = 5
    speed = 50
    hearts = 1
    enemy_image = ''

    def __init__(self, x, y):
        super().__init__(self.enemy_image, x, y)
        self.velocity_x = self.speed
        self.velocity_y = self.speed
        self.hearts = self.hearts

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def on_collision_snowball(self, snowball: Snowball):
        self.hearts -= 1
        if self.hearts <= 0:
            self.space.remove(self)
        self.space.remove(snowball)


class BigEnemy(Enemy):
    speed = 50
    hearts = 2
    enemy_image = ENEMY_BIG_IMAGE


class FastEnemy(Enemy):
    speed = 100
    hearts = 1
    enemy_image = ENEMY_FAST_IMAGE

