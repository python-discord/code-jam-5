import weakref

import pyglet


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

    def add_to_space(self, space):
        self.batch = space.batch
        super().add_to_space(space)

    def remove_from_space(self):
        self.batch = None
        super().remove_from_space()
