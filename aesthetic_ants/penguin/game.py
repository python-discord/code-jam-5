import pyglet

from .constants import CollisionType
from .enemy import BigEnemy, FastEnemy
from .player import Player
from .resources import LEVEL_1
from .snowball import Snowball
from .space import Space
from .tile_layer import TileLayer
from .ui import GameOverScreen, ScoreLabel
from .utils import keys


class Game(pyglet.window.Window):
    score = 0

    def __init__(self, *, fps=120, **kwargs):
        super().__init__(caption='Penguin Snowball', **kwargs)
        self.is_over = False
        self.fps = fps

        self.player = Player(self.width / 2, self.height / 2)
        self.player.game_over = self.game_over

        self.space = self.create_space()
        self.space.add(self.player)
        for _ in range(5):
            self.space.add(BigEnemy(10, 5))
            self.space.add(FastEnemy(15, 5))

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
        tiles.load_tiles(LEVEL_1)

        self.space.add_collision_handler(CollisionType.SNOWBALL,
                                         CollisionType.TILE_LAYER,
                                         tiles.collide_tiles,
                                         lambda _, _1: True)

        self.space.add_collision_handler(CollisionType.ENEMY,
                                         CollisionType.TILE_LAYER,
                                         tiles.collide_tiles,
                                         lambda _, _1: True)

        self.space.add_collision_handler(CollisionType.PLAYER,
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
        self.game_over(fell=False)

    def game_over(self, fell=False):
        if not self.is_over:
            self.is_over = True
            game_over_screen = GameOverScreen(self)
            self.ui_space.add(game_over_screen)
            if fell:
                self.space.remove(self.player)
                self.remove_handlers(self.player)

    def on_collision_snowball_enemy(self, snowball, enemy):
        if not self.is_over:
            self.score += enemy.score
            self.score_label.label.text = str(self.score)

        enemy.on_collision_snowball(snowball)
