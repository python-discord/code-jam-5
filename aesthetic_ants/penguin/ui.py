import pyglet

from .object import Object


class GameOverScreen(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("Game Over!",
                                       font_name="Times New Roman",
                                       font_size=36,
                                       x=window.width // 2,
                                       y=window.height // 2,
                                       anchor_x='center',
                                       anchor_y='center')

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch


class ScoreLabel(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("0",
                                       font_name="Times New Roman",
                                       font_size=18,
                                       x=10,
                                       y=window.height - 10,
                                       anchor_x='left',
                                       anchor_y='top')

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch
