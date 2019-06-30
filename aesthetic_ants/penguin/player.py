import pyglet


class Player(pyglet.sprite.Sprite):
    def __init__(self):
        player_image = pyglet.resource.image("penguin.png")
        super().__init__(player_image)

    def update(self, **kwargs):
        super().update(**kwargs)

    def on_mouse_motion(self, x, y, dx, dy):
        pass
