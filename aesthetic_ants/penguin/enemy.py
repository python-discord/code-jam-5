import pyglet
import random

from .object import PhysicalObject


class Enemy(PhysicalObject):

    def __init__(self):
        enemy_image = pyglet.resource.image('circle.png')
        enemy_image.width = 50
        enemy_image.height = 50
        super().__init__(enemy_image)
        self.velocity_x = random.randint(0, 100)
        self.velocity_y = random.randint(0, 100)

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
