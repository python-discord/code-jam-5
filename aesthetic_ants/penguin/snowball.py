from math import radians

from .constants import CollisionType
from .object import PhysicalObject
from .resources import ROCKET_IMAGE, SNOWBALL_IMAGE, SNOWSPLOSION_IMAGE
from .utils import vector_from_angle


__all__ = [
    'Snowball',
    'RocketBall',
    'Snowsplosion',
]


class Projectile(PhysicalObject):
    """Base class for all projectiles"""

    collision_type = CollisionType.SNOWBALL

    def on_collision_enemy(self, enemy):
        enemy.on_collision_snowball(self)


class Snowball(Projectile):
    def __init__(self, x, y, angle, speed, image=None):
        if image is None:
            image = SNOWBALL_IMAGE

        super().__init__(img=image, x=x, y=y)

        self.rotation = angle

        velocity_x, velocity_y = vector_from_angle(-radians(angle), speed)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def on_collision_enemy(self, enemy):
        super().on_collision_enemy(enemy)
        self.space.remove(self)


class RocketBall(Snowball):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, image=ROCKET_IMAGE, **kwargs)

    def on_collision_enemy(self, enemy):
        super().on_collision_enemy(enemy)
        self.space.add(Snowsplosion(self.x, self.y))
        self.space.remove(self)


class Snowsplosion(PhysicalObject):
    collision_type = CollisionType.SNOWSPLOSION

    def __init__(self, x, y):
        super().__init__(img=SNOWSPLOSION_IMAGE, x=x, y=y)
        self.lethal = True

    def collides_with(self, entity):
        if not self.lethal:
            return False

        return super().collides_with(entity)

    def update(self, dt):
        self.opacity *= 0.8

        if self.opacity <= 128:
            self.lethal = False

        if self.opacity <= 5:
            self.space.remove(self)

    def on_collision_enemy(self, enemy):
        self.space.remove(enemy)
