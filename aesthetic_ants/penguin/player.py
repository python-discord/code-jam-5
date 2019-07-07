from math import degrees

import pyglet.window.key as key
import pyglet.window.mouse as mouse

from .constants import CollisionType, TileType
from .object import PhysicalObject
from .resources import PLAYER_IMAGE
from .utils import angle_between, keys
from .weapon import Weapon


FALL_RATE = 1
FALL = 24
FALL_RATIO = 100


class Player(PhysicalObject):
    speed = 90
    collision_type = CollisionType.PLAYER
    falling = 0
    previous_coordinates = None

    def __init__(self, x, y):
        super().__init__(PLAYER_IMAGE, x=x, y=y)
        self.original_width = PLAYER_IMAGE.width
        self.original_height = PLAYER_IMAGE.height

        self.weapon = Weapon()

    def update(self, dt):
        if self.falling > 0:
            if self.falling < 4 * FALL_RATE:
                self.falling = 0
            else:
                self.falling -= 4 * FALL_RATE
            self.update_size()

        self.previous_coordinates = (self.x, self.y)

        if keys[key.W]:
            self.y += dt * self.speed
        if keys[key.S]:
            self.y -= dt * self.speed
        if keys[key.A]:
            self.x -= dt * self.speed
        if keys[key.D]:
            self.x += dt * self.speed

    def fire(self):
        for bullet in self.weapon.get_projectiles(self.x, self.y, self.rotation):
            self.space.add(bullet)

    def on_mouse_motion(self, x, y, dx, dy):
        self.rotation = degrees(angle_between(self.x, self.y, x, y))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.fire()

    def collide_tile(self, tile):
        if tile.tile_type == TileType.WATER:
            self.falling += FALL_RATE
            self.update_size()
            if self.falling > FALL:
                self.game_over(True)
        elif tile.tile_type == TileType.WALL:
            self.x, self.y = self.previous_coordinates

    def update_size(self):
        self.image.width = max(1, self.original_width * (1 - (self.falling / FALL_RATIO)))
        self.image.height = max(1, self.original_height * (1 - (self.falling / FALL_RATIO)))
