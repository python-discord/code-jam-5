import pyglet

from .snowball import RocketBall, Snowball


class Weapon:
    fire_delay = 0.25
    projectile_speed = 600
    unlock_score = 0

    def __init__(self):
        self.locked = True
        self.firing = False

    def reload(self, dt):
        self.firing = False

    def get_projectiles(self, x, y, angle):
        """Generates projectiles for the weapon"""
        raise NotImplementedError

    def fire(self, x, y, angle):
        """Fires the weapon and returns an iterable of bullets

        Returns an empty list if the weapon is still firing.
        """

        if self.firing:
            return []

        self.firing = True
        pyglet.clock.schedule_once(self.reload, self.fire_delay)
        return self.get_projectiles(x, y, angle)


class Hand(Weapon):
    locked = False

    def get_projectiles(self, x, y, angle):
        yield Snowball(x, y, angle, self.projectile_speed)


class SnowSpread(Weapon):
    fire_delay = 0.625
    unlock_score = 1000

    def get_projectiles(self, x, y, angle):
        for i in range(-2, 3):
            yield Snowball(x, y, angle + 10 * i, self.projectile_speed)


class RocketPropelledSnowball(Weapon):
    fire_delay = 1
    unlock_score = 10000

    def get_projectiles(self, x, y, angle):
        yield RocketBall(x, y, angle, self.projectile_speed)
