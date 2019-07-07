import pyglet
from pyqtree import Index
from config import *
from config import game_width, game_height
from math import ceil

# 640x640 makes it easier to draw tiles
game_window = pyglet.window.Window(width=game_width, height=game_height)

# fps_display = pyglet.window.FPSDisplay(game_window)

time_display = pyglet.clock.ClockDisplay()

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
        image = pyglet.image.load('assets/char.png')
        self.sprite_grid = pyglet.image.ImageGrid(image, 32, 27) #Load grid

        #Split the grid into subsections
        self.sprite_down = [self.sprite_grid[31, 1], self.sprite_grid[31, 2]]
        self.sprite_up = [self.sprite_grid[31, 7], self.sprite_grid[31, 8]]
        self.sprite_right = [self.sprite_grid[31, 3].get_texture(), self.sprite_grid[31, 5].get_texture()]

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
            self.current_sprite = player.sprite_grid[31, 0]

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

cut_scenes = {}
sound_list = {}
music_list = {}

current_display = "zone"
