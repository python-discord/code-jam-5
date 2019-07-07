import pyglet

from .object import Object
from .space import Space


SCORE_POS = (20, 15)
WEAPON_POS = (64, 32)


class UiSpace(Space):
    def __init__(self):
        super().__init__()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)


class ShadowedLabel:
    def __init__(self, space, text, x, y, color, **kwargs):
        self.label = pyglet.text.Label(text,
                                       color=color,
                                       x=x,
                                       y=y,
                                       group=space.foreground,
                                       **kwargs)

        self.shadow = pyglet.text.Label(text,
                                        color=(0, 0, 0, 255),
                                        x=x + 1,
                                        y=y - 1,
                                        group=space.background,
                                        **kwargs)

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, text):
        self.label.text = text
        self.shadow.text = text

    @property
    def batch(self):
        return self.label.batch

    @batch.setter
    def batch(self, batch):
        self.label.batch = batch
        self.shadow.batch = batch


class GameOverScreen(Object):
    def __init__(self, window, space):
        self.label = ShadowedLabel(space,
                                   "Game Over!",
                                   font_name="Times New Roman",
                                   font_size=36,
                                   color=(255, 0, 0, 255),
                                   x=window.width // 2,
                                   y=window.height // 2,
                                   anchor_x='center',
                                   anchor_y='center')

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch


class ScoreLabel(Object):
    def __init__(self, window, space):
        self.label = ShadowedLabel(space,
                                   "0",
                                   font_name="Times New Roman",
                                   font_size=18,
                                   color=(255, 255, 0, 255),
                                   x=SCORE_POS[0],
                                   y=window.height - SCORE_POS[1],
                                   anchor_x='left',
                                   anchor_y='top')

    def set_label(self, value):
        self.label.text = str(value)

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch


class WeaponIndicator(Object):
    def __init__(self, window, space, player):
        self.player = player
        self.label = ShadowedLabel(space,
                                   self.weapon_text(self.player.weapon),
                                   font_name="Times New Roman",
                                   font_size=32,
                                   color=(255, 0, 255, 255),
                                   x=window.width - WEAPON_POS[0],
                                   y=0,
                                   anchor_x='right',
                                   anchor_y='bottom')

    def weapon_text(self, weapon):
        if weapon is None:
            return ''

        if weapon.reloading:
            return 'Reloading...'

        if weapon.ammo is None:
            return '\u221e'

        if weapon.ammo == 0:
            return 'Reload!'

        return str(weapon.ammo)

    def update(self, dt):
        self.label.text = self.weapon_text(self.player.weapon)

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch
