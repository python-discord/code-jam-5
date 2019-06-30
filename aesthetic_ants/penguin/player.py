from math import degrees

import pyglet
import pyglet.window.key as key

from .utils import angle_between, loader, keys


class Player(pyglet.sprite.Sprite):
    def __init__(self, x, y):
        player_image = loader.image("penguin.png")

        # Rotate about the center
        player_image.anchor_x = player_image.width // 2
        player_image.anchor_y = player_image.height // 2

        super().__init__(player_image, x=x, y=y)

    def update(self, **kwargs):
        super().update(**kwargs)

        if keys[key.W]:
            self.y += 1
        if keys[key.S]:
            self.y -= 1
        if keys[key.A]:
            self.x -= 1
        if keys[key.D]:
            self.x += 1

    def on_mouse_motion(self, x, y, dx, dy):
        self.rotation = degrees(angle_between(self.x, self.y, x, y))
