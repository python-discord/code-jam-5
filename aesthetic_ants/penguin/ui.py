import pyglet

from .object import Object
from .space import Space


SCORE_POS = (20, 15)


class UiSpace(Space):
    def __init__(self):
        super().__init__()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)


class GameOverScreen(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("Game Over!",
                                       font_name="Times New Roman",
                                       font_size=36,
                                       color=(255, 0, 0, 255),
                                       x=window.width // 2,
                                       y=window.height // 2,
                                       anchor_x='center',
                                       anchor_y='center')

        self.shadow = pyglet.text.Label("Game Over!",
                                        font_name="Times New Roman",
                                        font_size=36,
                                        color=(0, 0, 0, 255),
                                        x=(window.width // 2) + 1,
                                        y=(window.height // 2) - 1,
                                        anchor_x='center',
                                        anchor_y='center')

    def add_to_space(self, space):
        super().add_to_space(space)

        self.shadow.batch = space.batch
        self.shadow.group = space.background

        self.label.batch = space.batch
        self.label.group = space.foreground


class ScoreLabel(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("0",
                                       font_name="Times New Roman",
                                       font_size=18,
                                       color=(255, 255, 0, 255),
                                       x=SCORE_POS[0],
                                       y=window.height - SCORE_POS[1],
                                       anchor_x='left',
                                       anchor_y='top')

        self.shadow = pyglet.text.Label("0",
                                        font_name="Times New Roman",
                                        font_size=18,
                                        color=(0, 0, 0, 255),
                                        x=SCORE_POS[0] + 1,
                                        y=window.height - SCORE_POS[1] - 1,
                                        anchor_x='left',
                                        anchor_y='top')

    def set_label(self, value):
        self.label.text = str(value)
        self.shadow.text = str(value)

    def add_to_space(self, space):
        super().add_to_space(space)

        self.shadow.batch = space.batch
        self.shadow.group = space.background

        self.label.batch = space.batch
        self.label.group = space.foreground
