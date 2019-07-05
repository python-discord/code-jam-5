import pyglet

from .constants import CollisionType
from .enemy import Enemy
from .player import Player
from .space import Space
from .utils import keys


class Game(pyglet.window.Window):
    def __init__(self, *, fps=120, **kwargs):
        super().__init__(caption='Penguin Snowball', **kwargs)
        self.fps = fps

        self.player = Player(self.width / 2, self.height / 2)

        self.space = self.create_space()
        self.space.add(self.player)
        for _ in range(5):
            self.space.add(Enemy())

        # Add handlers
        self.push_handlers(self.player)
        self.push_handlers(keys)

    def create_space(self) -> Space:
        """Returns a space usable for the game"""

        space = Space()

        space.add_collision_handler(CollisionType.PLAYER,
                                    CollisionType.ENEMY,
                                    Player.on_collision_enemy,
                                    Player.collides_with)

        space.add_collision_handler(CollisionType.ENEMY,
                                    CollisionType.SNOWBALL,
                                    Enemy.on_collision_snowball,
                                    Enemy.collides_with)

        return space

    def on_draw(self):
        self.clear()
        self.space.draw()

    def update(self, dt):
        self.space.update(dt)

    def run(self):
        """Runs the game"""

        pyglet.clock.schedule_interval(self.update, 1/self.fps)
        pyglet.app.run()
