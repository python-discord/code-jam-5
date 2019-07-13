import weakref

import pyglet

from .utils import circles_collide


class Object:
    """Base class for all objects"""

    space = None
    collision_type = None

    def add_to_space(self, space):
        self.space = weakref.proxy(space)

    def remove_from_space(self):
        self.space = None

    def update(self, dt):
        pass


class PhysicalObject(Object, pyglet.sprite.Sprite):
    """Base class for all tangible objects (objects with sprites)"""
    collision_leniency = 0.85

    def add_to_space(self, space):
        self.batch = space.batch
        super().add_to_space(space)

    def remove_from_space(self):
        self.batch = None
        super().remove_from_space()

    def collides_with(self, other) -> bool:
        """
        Called to determine if this collider collides with another
        """
        return circles_collide(self.x,
                               self.y,
                               self.width * self.collision_leniency / 2,
                               other.x,
                               other.y,
                               other.width * self.collision_leniency / 2)
