from math import degrees

import pyglet.window.key as key
import pyglet.window.mouse as mouse

from .constants import CollisionType
from .enemy import Enemy
from .object import PhysicalObject
from .resources import PLAYER_IMAGE
from .utils import angle_between, keys
from .weapon import Weapon


class Player(PhysicalObject):
    speed = 90
    collision_type = CollisionType.PLAYER

    def __init__(self, x, y):
        super().__init__(PLAYER_IMAGE, x=x, y=y)

        self.weapon = Weapon()

    def update(self, dt):
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

    def on_collision_enemy(self, enemy: Enemy):
        """
        What happens when a player runs into an enemy
        """
        raise NotImplementedError
