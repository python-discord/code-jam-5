from math import degrees

import pyglet.window.key as key
import pyglet.window.mouse as mouse

from .constants import CollisionType, TileType
from .object import PhysicalObject
from .resources import PLAYER_IMAGE
from .utils import angle_between, keys
from .weapon import Hand, RocketPropelledSnowball, SnowSpread


FALL_RATE = 60
FALL_SCALE = 60
FALL_MAX = 30


class Player(PhysicalObject):
    speed = 90
    collision_type = CollisionType.PLAYER
    falling = 0
    water_tiles = 0
    previous_coordinates = None

    def __init__(self, x, y):
        super().__init__(PLAYER_IMAGE, x=x, y=y)
        self.original_width = PLAYER_IMAGE.width
        self.original_height = PLAYER_IMAGE.height

        self.weapons = {
            key._1: Hand(),
            key._2: SnowSpread(),
            key._3: RocketPropelledSnowball(),

        }
        self.weapon = self.weapons[key._1]
        self.firing = False

    def update(self, dt):
        # Fall into water if there's too much under our feet
        if self.water_tiles >= 4:
            self.falling += FALL_RATE * dt

        # If we're on full land, climb back up
        if self.water_tiles == 0 and self.falling > 0:
            self.falling -= FALL_RATE * 2 * dt

        if self.falling:
            self.falling += FALL_RATE * dt
            self.update_size()

        if self.falling > FALL_MAX:
            self.game_over(fell=True)

        self.water_tiles = 0

        self.previous_coordinates = (self.x, self.y)

        if keys[key.W]:
            self.y += dt * self.speed
        if keys[key.S]:
            self.y -= dt * self.speed
        if keys[key.A]:
            self.x -= dt * self.speed
        if keys[key.D]:
            self.x += dt * self.speed

        if self.firing:
            self.fire()

    def fire(self):
        for bullet in self.weapon.fire(self.x, self.y, self.rotation):
            self.space.add(bullet)

    def unlock_weapons(self, score):
        for weapon in self.weapons.values():
            if score >= weapon.unlock_score:
                weapon.locked = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.rotation = degrees(angle_between(self.x, self.y, x, y))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.rotation = degrees(angle_between(self.x, self.y, x, y))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.firing = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.firing = False

    def on_key_press(self, button, modifiers):
        if button == key.R:
            self.weapon.reload()
            return

        # Avoid switching weapons while our current weapon is reloading
        # as that might be cheaty
        if self.weapon.reloading:
            return

        weapon = self.weapons.get(button)
        if not weapon:
            return

        if weapon.locked:
            return

        self.weapon = weapon

    def collide_tile(self, tile):
        if tile.tile_type == TileType.WATER:
            self.water_tiles += 1
        elif tile.tile_type == TileType.WALL:
            self.x, self.y = self.previous_coordinates

    def update_size(self):
        self.image.width = max(1, self.original_width * (1 - (self.falling / FALL_SCALE)))
        self.image.height = max(1, self.original_height * (1 - (self.falling / FALL_SCALE)))
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
