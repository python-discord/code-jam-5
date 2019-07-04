from math import radians

from .snowball import Snowball
from .utils import vector_from_angle


class Weapon:
    projectile_speed = 600

    @staticmethod
    def convert_angle(angle):
        """Converts the angle from pyglet units (CCW, degrees)
        to math units (CW, radians)
        """

        return -radians(angle)

    def get_projectiles(self, x, y, angle):
        converted = self.convert_angle(angle)
        velocity_x, velocity_y = vector_from_angle(converted, self.projectile_speed)

        bullet = Snowball(x, y, velocity_x, velocity_y)
        bullet.rotation = angle

        yield bullet
