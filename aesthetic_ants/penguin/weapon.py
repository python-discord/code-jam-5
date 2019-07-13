import pyglet

from .resources import RPG_ICON, SHOTGUN_ICON, SNOWBALL_ICON
from .snowball import RocketBall, Snowball


class Weapon:
    fire_delay = 0.25
    reload_delay = 1.5
    projectile_speed = 600
    unlock_score = 0
    clip_size = None
    icon = None

    def __init__(self):
        self.locked = True
        self.firing = False
        self.reloading = False
        self.ammo = self.clip_size

    def get_projectiles(self, x, y, angle):
        """Generates projectiles for the weapon"""
        raise NotImplementedError

    def _reload(self, dt):
        self.ammo = self.clip_size
        self.reloading = False

    def reload(self):
        if self.clip_size is None:
            return

        self.reloading = True
        pyglet.clock.schedule_once(self._reload, self.reload_delay)

    def _fire(self, dt):
        self.firing = False

    def fire(self, x, y, angle):
        """Fires the weapon and returns an iterable of bullets

        Returns an empty list if the weapon is still firing.
        """

        if self.firing:
            return []

        if self.ammo is not None:
            if self.ammo <= 0:
                return []
            self.ammo -= 1

        self.firing = True
        pyglet.clock.schedule_once(self._fire, self.fire_delay)
        return self.get_projectiles(x, y, angle)


class Hand(Weapon):
    locked = False
    icon = SNOWBALL_ICON

    def get_projectiles(self, x, y, angle):
        yield Snowball(x, y, angle, self.projectile_speed)


class SnowSpread(Weapon):
    fire_delay = 0.625
    unlock_score = 1000
    clip_size = 16
    icon = SHOTGUN_ICON

    def get_projectiles(self, x, y, angle):
        for i in range(-2, 3):
            yield Snowball(x, y, angle + 10 * i, self.projectile_speed)


class RocketPropelledSnowball(Weapon):
    fire_delay = 1
    unlock_score = 10000
    clip_size = 4
    icon = RPG_ICON

    def get_projectiles(self, x, y, angle):
        yield RocketBall(x, y, angle, self.projectile_speed)
