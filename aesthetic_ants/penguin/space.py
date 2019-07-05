import itertools
import typing

import pyglet

from .object import Object

ObjectCallback = typing.Callable[[Object, Object], typing.Any]


class Space:
    """Space that contains all objects"""

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.handlers = {}

        self.objects = []
        self._to_add = set()
        self._to_remove = set()

        self._updating = False

    def _add(self, obj):
        obj.add_to_space(self)
        self.objects.append(obj)

    def add(self, obj: Object):
        """Adds an object from the space"""
        if self._updating:
            self._to_add.add(obj)
        else:
            self._add(obj)

    def _remove(self, obj):
        obj.remove_from_space()
        self.objects.remove(obj)

    def remove(self, obj: Object):
        """Removes an object from the space"""
        if self._updating:
            self._to_remove.add(obj)
        else:
            self._remove(obj)

    def update(self, dt: float):
        """Updates all the objects"""

        self._updating = True

        for obj in self.objects:
            obj.update(dt)

        # Check if any collisions occurred.
        for obj1, obj2 in itertools.combinations(self.objects, 2):
            type1 = obj1.collision_type
            type2 = obj2.collision_type

            collision_handler = self.handlers.get((type1, type2))
            if collision_handler is None:
                obj1, obj2 = obj2, obj1
                collision_handler = self.handlers.get((type2, type1))
                continue

            if collision_handler is None:
                continue

            detect, handler = collision_handler
            if detect(obj1, obj2):
                handler(obj1, obj2)

        self._updating = False

        for obj in self._to_add:
            self.add(obj)

        for obj in self._to_remove:
            self.remove(obj)

        # Clear both pending stuff
        self._to_add.clear()
        self._to_remove.clear()

    def draw(self):
        """Draws all the objects"""
        self.batch.draw()

    def add_collision_handler(
        self,
        type1,
        type2,
        handler: ObjectCallback,
        detection: ObjectCallback
    ):
        """Adds a collision detection and handler callback to the space"""
        self.handlers[type1, type2] = (detection, handler)

    def remove_collision_handler(self, type1, type2):
        """Removes a collision detection and handler callback from the space"""
        self.handlers.pop((type1, type2), None)
