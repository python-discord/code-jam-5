import math
import random

import pyglet

from .snowball import Snowball
from .constants import CollisionType, TileType
from .object import PhysicalObject
from .resources import ENEMY_BIG_IMAGE, ENEMY_FAST_IMAGE, ENEMY_TRUCK_IMAGE
from .utils import normalized


class Enemy(PhysicalObject):
    collision_type = CollisionType.ENEMY
    score = 5

    unstun_time = 0.5
    speed_min = 50
    speed_max = 50
    hearts = 1
    enemy_image = ''

    def __init__(self, x, y, player):
        super().__init__(self.enemy_image, x, y)
        self.velocity_x = 1
        self.velocity_y = 1
        self.speed = random.uniform(self.speed_min, self.speed_max)

        self.tracking = True
        self.player = player

    def update(self, dt):
        if self.tracking:
            vx = self.player.x - self.x
            vy = self.player.y - self.y
            self.velocity_x, self.velocity_y = normalized(vx, vy)

        self.rotation = -math.degrees(math.atan2(self.velocity_y, self.velocity_x))

        self.x += self.velocity_x * self.speed * dt
        self.y += self.velocity_y * self.speed * dt

    def unstun(self, *args):
        self.tracking = True

    def stun(self):
        self.tracking = False
        pyglet.clock.schedule_once(self.unstun, self.unstun_time)

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
                    self.stun()
                    self.velocity_x *= -1
                if tile.x < self.x and self.velocity_x < 0:
                    self.stun()
                    self.velocity_x *= -1

            if tile_offset_x < tile_offset_y < self.height * self.collision_leniency // 2:
                if tile.y > self.y and self.velocity_y > 0:
                    self.stun()
                    self.velocity_y *= -1
                if tile.y < self.y and self.velocity_y < 0:
                    self.stun()
                    self.velocity_y *= -1


class NormalEnemy(Enemy):
    speed_min = 50
    speed_max = 100
    enemy_image = ENEMY_FAST_IMAGE


class BigEnemy(Enemy):
    speed_min = 20
    speed_max = 50
    hearts = 2
    enemy_image = ENEMY_BIG_IMAGE


class FastEnemy(Enemy):
    speed_min = 100
    speed_max = 250
    hearts = 1
    enemy_image = ENEMY_FAST_IMAGE


class Truck(Enemy):
    speed_min = 20
    speed_max = 40
    hearts = 10
    score = 100
    enemy_image = ENEMY_TRUCK_IMAGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = random.uniform(0.5, 1)

    def spawn_enemy(self):
        clses = [NormalEnemy, BigEnemy, FastEnemy]
        weights = [0.5, 0.2, 0.2]

        cls = random.choices(clses, weights)[0]
        self.space.add(cls(self.x, self.y, self.player))

        self.delay = random.uniform(0.5, 1)

    def update(self, dt):
        super().update(dt)

        self.delay -= dt
        if self.delay <= 0:
            self.spawn_enemy()
