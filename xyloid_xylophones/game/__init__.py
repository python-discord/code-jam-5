import pyglet
from pyglet import gl
from pyqtree import Index
from config import *
from config import game_width, game_height, char_sheet_cols, char_sheet_rows, sprite_row, sprite_up_col, sprite_down_col, sprite_right_col
from math import ceil
import os
from pathlib import Path

from .gamemap import Map


# Help
assets_path = os.path.split(os.path.realpath(__file__))[0] + '/../assets/'
grid = pyglet.image.load(assets_path + 'sheet.png')
b1 = grid.get_region(0,0,64,64)
b2 = grid.get_region(64,0,64,64)
b3 = grid.get_region(128,0,64,64)
b4 = grid.get_region(192,0,64,64)
b5 = grid.get_region(256,0,64,64)
b6 = grid.get_region(320,0,64,64)
b7 = grid.get_region(384,0,64,64)
b8 = grid.get_region(448,0,64,64)
b9 = grid.get_region(512,0,64,64)
b10 = grid.get_region(576,0,64,64)
b11 = grid.get_region(640,0,64,64)
b12 = grid.get_region(704,0,64,64)
b13 = grid.get_region(768,0,64,64)
b14 = grid.get_region(832,0,64,64)
b15 = grid.get_region(896,0,64,64)
b16 = grid.get_region(960,0,64,64)
b17 = grid.get_region(1024,0,64,64)
b18 = grid.get_region(1088,0,64,64)
b19 = grid.get_region(1152,0,64,64)
b20 = grid.get_region(1216,0,64,64)
level1map = Map(assets_path + 'myfile.map',
        {
            1: b1,
            2: b2,
            3: b3,
            4: b4,
            5:b5,
            6:b6,
            7:b7,
            8:b8,
            9:b9,
            10:b10,
            11:b11,
            12:b12,
            13:b13,
            14:b14,
            15:b15,
            16:b16,
            17:b17,
            18:b18,
            19:b19,
            20:b20})

# 640x640 makes it easier to draw tiles
game_window = pyglet.window.Window(width=game_width, height=game_height)

time_display = pyglet.window.FPSDisplay(game_window)

media = pyglet.media.Player()

#List of current pressed keys
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
        self.sprite_switch = 0 #Alternates images to create movement effect
        self.scale_x = 1
        self.adjustment = 0
    def load_player(self):
        '''Load all of the sprite sets for the player'''
        image = pyglet.image.load(os.path.join(Path(__file__).resolve().parents[1], Path('assets/char.png')))

        self.sprite_grid = pyglet.image.ImageGrid(image, char_sheet_rows, char_sheet_cols) #Load grid

        #Split the grid into subsections
        self.sprite_down = [self.sprite_grid[sprite_row, sprite_down_col], self.sprite_grid[sprite_row, sprite_down_col + 1]]
        self.sprite_up = [self.sprite_grid[sprite_row, sprite_up_col], self.sprite_grid[sprite_row, sprite_up_col + 1]]
        self.sprite_right = [self.sprite_grid[sprite_row, sprite_right_col], self.sprite_grid[sprite_row, sprite_right_col+1]]
        self.sprite = pyglet.sprite.Sprite(img=self.sprite_down[0]) #Initialize player
        self.update_sprite()

    def update_sprite(self, sprite="default"):
        '''Update the sprite for the player based on input'''
        #Reset adjustments
        self.scale_x = 1
        self.sprite.image.anchor_x = 0

        #Adjust sprite for movement
        if (sprite=="down"):
            self.current_sprite = player.sprite_down[self.sprite_switch]
        elif (sprite=="up"):
            self.current_sprite = player.sprite_up[self.sprite_switch]
        elif (sprite=="right"):
            self.current_sprite = player.sprite_right[self.sprite_switch]
        elif (sprite=="left"):
            self.scale_x = -1 #Flip the image around
            self.adjustment = self.sprite.image.width
            self.sprite.image.anchor_x = self.sprite.image.width // 2
            self.current_sprite = self.sprite_right[self.sprite_switch]
        else:
            #Default sprite
            self.current_sprite = self.sprite_down[0]

        #Alternate sprite chosen
        if (self.sprite_switch == 0):
            self.sprite_switch = 1
        else:
            self.sprite_switch = 0

        #Update the player
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

player = Player(player_name)
# static center of player square
player.center_x = 4*64
player.center_y = 4*64
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
