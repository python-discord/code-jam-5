import random

from .snowball import Snowball
from .constants import CollisionType
from .object import Object
from .object import PhysicalObject
from .resources import ENEMY_BIG_IMAGE, ENEMY_FAST_IMAGE


class Enemy(PhysicalObject):
    collision_type = CollisionType.ENEMY
    score = 5

    def __init__(self, x, y, speed, hearts, enemy_image):
        super().__init__(enemy_image, x, y)
        self.velocity_x = speed
        self.velocity_y = speed
        self.hearts = hearts
        self.hit_count = 0

    def update(self, dt):
        None
        #self.x += self.velocity_x * dt
        #self.y += self.velocity_y * dt

    def on_collision_snowball(self, snowball: Snowball):
        self.hit_count += 1
        if self.hit_count == self.hearts:
            self.space.remove(self)
        self.space.remove(snowball)


class BigEnemy(Enemy):

    def __init__(self):
        self.speed = 50
        self.hearts = 2
        x = random.randint(1, 640)
        y = random.randint(1, 480)
        super().__init__(x, y, self.speed, self.hearts, ENEMY_BIG_IMAGE)


class FastEnemy(Enemy):

    def __init__(self):
        self.speed = 100
        self.hearts = 1
        x = random.randint(1, 640)
        y = random.randint(1, 480)
        super().__init__(x, y, self.speed, self.hearts, ENEMY_FAST_IMAGE)

