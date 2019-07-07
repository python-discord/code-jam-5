import random

from .object import Object


class Spawner(Object):
    def __init__(self, player):
        # Required for enemy tracking
        self.player = player

        self.spawn_points = []
        self.wave = None
        self.delay = 0
        self._done = False

    def add_spawn_point(self, x: float, y: float):
        """Adds a spawn point to the spawner"""
        self.spawn_points.append((x, y))

    def done(self) -> bool:
        """Return True if the spawner is done spawning, False otherwise"""
        return self._done

    def update(self, dt):
        if self.wave is None:
            return

        self._done = False

        if self.delay > 0:
            self.delay -= dt
            return

        for thing in self.wave:
            # TODO: Duck-type this
            if isinstance(thing, (int, float)):
                self.delay = thing
                break
            else:
                x, y = random.choice(self.spawn_points)
                self.space.add(thing(x, y, self.player))
        else:
            # We finished the wave!
            self._done = True
            self.wave = None
