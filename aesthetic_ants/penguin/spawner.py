import random

from .enemy import Enemy
from .object import Object


class Spawner(Object):
    def __init__(self):
        self.spawn_points = []

    def add_spawn_point(self, x, y):
        """Adds a spawn point to the spawner"""
        self.spawn_points.append((x, y))

    def update(self, dt):
        if random.random() > .05:
            return

        x, y = random.choice(self.spawn_points)
        self.space.add(Enemy(x, y))
