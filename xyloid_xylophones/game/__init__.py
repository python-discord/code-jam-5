import pyglet
from pyqtree import Index
from config import game_width, game_height, char_sheet_cols, char_sheet_rows, sprite_row, sprite_up_col, \
    sprite_down_col, sprite_right_col, zone_names, zone_width, zone_height, sprite_width, sprite_height
from os.path import join
from pathlib import Path

# sprite list of tiles
level_map = []

# map of no collision / collision
level_key = [False,
             False, False, False, False, True,
             True, True, False, False, True,
             True, True, False, False, False,
             True, True, True, True, True,
             False, False, False, False, True,
             True, True, False, False, True,
             True, True, False, False, False,
             True, True, True, False, False, True]

# 640x640 makes it easier to draw tiles
game_window = pyglet.window.Window(width=game_width, height=game_height)

time_display = pyglet.window.FPSDisplay(game_window)

media = pyglet.media.Player()

# List of current pressed keys
keys = set()


class Base:
    id: int = 0
    name: str = 'base_class'
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    collision: bool = False


class Zone(Base):
    index: Index

    def __init__(self, index):
        self.index = index


# player object
class Player(Base):
    sprite: str = 'char.png'

    def __init__(self, name):
        self.name = name
        self.sprite_switch = 0  # Alternates images to create movement effect
        self.scale_x = 1
        self.adjustment = 0
        self.action = None
        self.current_zone = 'desolate wasteland'
        self.dialog = ''

    def load_player(self):
        '''Load all of the sprite sets for the player'''
        # image = pyglet.image.load('assets/char.png')
        image = pyglet.image.load(join(Path(__file__).resolve().parents[1], Path('assets/char.png')))

        self.sprite_grid = pyglet.image.ImageGrid(image, char_sheet_rows, char_sheet_cols)  # Load grid

        # Split the grid into subsections
        self.sprite_down = [self.sprite_grid[sprite_row, sprite_down_col],
                            self.sprite_grid[sprite_row, sprite_down_col + 1]]
        self.sprite_up = [self.sprite_grid[sprite_row, sprite_up_col], self.sprite_grid[sprite_row, sprite_up_col + 1]]
        self.sprite_right = [self.sprite_grid[sprite_row, sprite_right_col],
                             self.sprite_grid[sprite_row, sprite_right_col + 1]]
        self.sprite = pyglet.sprite.Sprite(img=self.sprite_down[0])  # Initialize player
        self.update_sprite()

    def update_sprite(self, sprite="default"):
        '''Update the sprite for the player based on input'''
        # Reset adjustments
        self.scale_x = 1
        self.sprite.image.anchor_x = 0

        # Adjust sprite for movement
        if (sprite == "down"):
            self.current_sprite = player.sprite_down[self.sprite_switch]
        elif (sprite == "up"):
            self.current_sprite = player.sprite_up[self.sprite_switch]
        elif (sprite == "right"):
            self.current_sprite = player.sprite_right[self.sprite_switch]
        elif (sprite == "left"):
            self.scale_x = -1  # Flip the image around
            self.adjustment = self.sprite.image.width
            self.sprite.image.anchor_x = self.sprite.image.width // 2
            self.current_sprite = self.sprite_right[self.sprite_switch]
        else:
            # Default sprite
            self.current_sprite = self.sprite_down[0]

        # Alternate sprite chosen
        if (self.sprite_switch == 0):
            self.sprite_switch = 1
        else:
            self.sprite_switch = 0

        # Update the player
        self.sprite = pyglet.sprite.Sprite(img=self.current_sprite)
        self.sprite.scale = 4
        self.sprite.update(x=self.center_x + self.adjustment, y=self.center_y, scale_x=self.scale_x)


class Item(Player):
    state: int = -1  # -1 intangible, 0 container unopened, 1 container opened
    sound: str = 'default_sound'
    contains: str = 'default_nothing'


class Resource:
    full_path: str = ''
    stream: None
    data: None


zone_map = {}
for i in zone_names:
    zone_map[i] = Zone(Index(bbox=(-1024, -1024, 1024, 1024)))
    zone_map[i].name = i

player = Player('Steve')
# static center of player square
player.center_x = 4 * 64
player.center_y = 4 * 64
# center of all the squares aka 0,0
player.x = zone_width // 2
player.y = zone_height // 2
player.width = sprite_width
player.height = sprite_height
# handlers for player movement
player.x_vel = 0
player.y_vel = 0

tick = 0
elapsed_time = 0

scene_list = {}
sound_list = {}
music_list = {}

current_display = "zone"
