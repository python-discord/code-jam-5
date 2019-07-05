import pyglet
from math import radians

from .snowball import Snowball
from .utils import vector_from_angle


class Weapon:
    reload_delay = 0.25
    projectile_speed = 600

    def __init__(self):
        self.reloading = False

    @staticmethod
    def convert_angle(angle):
        """Converts the angle from pyglet units (CCW, degrees)
        to math units (CW, radians)
        """

        return -radians(angle)

    def reload(self, dt):
        self.reloading = False

    def get_projectiles(self, x, y, angle):
        """Generate projectiles for the weapon"""

        converted = self.convert_angle(angle)
        velocity_x, velocity_y = vector_from_angle(converted, self.projectile_speed)

        bullet = Snowball(x, y, velocity_x, velocity_y)
        bullet.rotation = angle

        yield bullet

    def fire(self, x, y, angle):
        """Fires the weapon and returns an iterable of bullets

        Returns an empty list if the weapon is still reloading.
        """

        if self.reloading:
            return []

        self.reloading = True
        pyglet.clock.schedule_once(self.reload, self.reload_delay)
        return self.get_projectiles(x, y, angle)
