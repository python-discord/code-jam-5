import random

from .snowball import Snowball
from .constants import CollisionType, TileType
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

    def collide_tile(self, tile):
        if tile.tile_type == TileType.WALL:
            tile_offset_x = abs(self.x - tile.x)
            tile_offset_y = abs(self.y - tile.y)

            if tile_offset_y < tile_offset_x < self.width * self.collision_leniency // 2:
                if tile.x > self.x and self.velocity_x > 0:
                    self.velocity_x *= -1
                if tile.x < self.x and self.velocity_x < 0:
                    self.velocity_x *= -1

            if tile_offset_x < tile_offset_y < self.height * self.collision_leniency // 2:
                if tile.y > self.y and self.velocity_y > 0:
                    self.velocity_y *= -1
                if tile.y < self.y and self.velocity_y < 0:
                    self.velocity_y *= -1


class BigEnemy(Enemy):
    speed = 50
    hearts = 2
    enemy_image = ENEMY_BIG_IMAGE


class FastEnemy(Enemy):
    speed = 100
    hearts = 1
    enemy_image = ENEMY_FAST_IMAGE
