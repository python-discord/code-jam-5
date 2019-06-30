import pyglet
from pyqtree import Index
from config import *
from random import random


# 640x640 makes it easier to draw tiles
game_window = pyglet.window.Window(width=640, height=640)

# fps_display = pyglet.window.FPSDisplay(game_window)

time_display = pyglet.clock.ClockDisplay()

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
    sprite: str = 'default_item'

    def __init__(self, name):
        self.name = name

class Item(Player):
    state: int = -1  # -1 intangible, 0 container unopened, 1 container opened
    sound: str = 'default_sound'
    contains: str = 'default_nothing'

zone_map = {}
for i in zone_names:
    zone_map[i] = Zone(Index(bbox=(0, 0, zone_width, zone_height)))
    zone_map[i].name = i
    zone_map[i].width = zone_width
    zone_map[i].height = zone_height

player = Player(player_name)
player.x = zone_width // 2
player.y = zone_height // 2

for i in zone_names:
    for x in range(0, 1024):
        random_item = Item('trash')
        random_item.x = int(random() * zone_width)
        random_item.y = int(random() * zone_height)
        random_item.width = sprite_width
        random_item.height = sprite_height
        random_item.collision = True
        if not zone_map[i].index.intersect(bbox=(random_item.x,
                                                 random_item.y,
                                                 random_item.x + random_item.width,
                                                 random_item.y + random_item.height)):
            zone_map[i].index.insert(random_item, bbox=(
                random_item.x,
                random_item.y,
                random_item.x+random_item.width,
                random_item.y+random_item.height)
                                 )
