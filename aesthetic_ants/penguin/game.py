import pyglet

from .constants import CollisionType
from .object import Object
from .player import Player
from .snowball import Snowball
from .space import Space
from .spawner import Spawner
from .tile_layer import TileLayer
from .utils import keys
from .wave import Wave


class Game(pyglet.window.Window):
    score = 0

    def __init__(self, *, fps=120, **kwargs):
        super().__init__(caption='Penguin Snowball', **kwargs)
        self.is_over = False
        self.fps = fps

        self.space = self.create_space()

        self.player = Player(self.width / 2, self.height / 2)
        self.space.add(self.player)

        self.spawner = Spawner()
        self.spawner.add_spawn_point(0, 0)
        self.spawner.wave = Wave.load('resources/waves/1.wave')
        self.space.add(self.spawner)

        # Create background layer
        self.tiles = self.create_tiles()

        self.space.add(self.tiles)

        # Add handlers
        self.push_handlers(self.player)
        self.push_handlers(keys)

        # Create UI
        self.ui_space = self.create_ui()

        self.score_label = ScoreLabel(self)
        self.ui_space.add(self.score_label)

    def create_space(self) -> Space:
        """Returns a space usable for the game"""

        space = Space()

        space.add_collision_handler(CollisionType.PLAYER,
                                    CollisionType.ENEMY,
                                    self.on_collision_player_enemy,
                                    Player.collides_with)

        space.add_collision_handler(CollisionType.SNOWBALL,
                                    CollisionType.ENEMY,
                                    self.on_collision_snowball_enemy,
                                    Snowball.collides_with)

        return space

    def create_tiles(self) -> TileLayer:
        """Creates the tile background layer"""
        tiles = TileLayer(0, 0)
        tiles.load_tiles("resources/levels/1.level")

        self.space.add_collision_handler(CollisionType.SNOWBALL,
                                         CollisionType.TILE_LAYER,
                                         tiles.collide_tiles,
                                         lambda _, _1: True)

        return tiles

    def create_ui(self) -> Space:
        """Returns the user interface space"""

        space = Space()

        return space

    def on_draw(self):
        self.clear()
        self.tiles.draw()
        self.space.draw()
        self.ui_space.draw()

    def update(self, dt):
        self.space.update(dt)
        self.ui_space.update(dt)

    def run(self):
        """Runs the game"""

        pyglet.clock.schedule_interval(self.update, 1/self.fps)
        pyglet.app.run()

    def on_collision_player_enemy(self, player, enemy):
        """When a player collides with an enemy, end the game"""
        if not self.is_over:
            self.is_over = True
            game_over_screen = GameOverScreen(self)
            self.ui_space.add(game_over_screen)

    def on_collision_snowball_enemy(self, snowball, enemy):
        if not self.is_over:
            self.score += enemy.score
            self.score_label.label.text = str(self.score)

        enemy.on_collision_snowball(snowball)


class GameOverScreen(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("Game Over!",
                                       font_name="Times New Roman",
                                       font_size=36,
                                       x=window.width // 2,
                                       y=window.height // 2,
                                       anchor_x='center',
                                       anchor_y='center')

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch


class ScoreLabel(Object):
    def __init__(self, window):
        self.label = pyglet.text.Label("0",
                                       font_name="Times New Roman",
                                       font_size=18,
                                       x=10,
                                       y=window.height - 10,
                                       anchor_x='left',
                                       anchor_y='top')

    def add_to_space(self, space):
        super().add_to_space(space)
        self.label.batch = space.batch
