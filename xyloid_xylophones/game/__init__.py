import pyglet
from pyqtree import Index
from config import *
from random import getrandbits


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
    zone_map[i] = Zone(Index(bbox=(-1024, -1024, 1024, 1024)))
    zone_map[i].name = i

player = Player(player_name)
player.center_x = 4*64
player.x = player.center_x
player.center_y = 5*64
player.y = player.center_y
player.width = sprite_width
player.height = sprite_height

for i in zone_names:
    for y in range(0, zone_height):
        for x in range(0, zone_width):
            item = Item('x%sy%s' % (x, y))
            item.y = y * sprite_height
            item.x = x * sprite_width
            item.width = sprite_width-1
            item.height = sprite_height-1
            item.collision = not getrandbits(1)
            if item.collision:
                item.color = (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
            else:
                item.color = (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)

            if not zone_map[i].index.intersect(bbox=(item.x,
                                                     item.y,
                                                     item.x + item.width,
                                                     item.y + item.height)):
                zone_map[i].index.insert(item, bbox=(
                    item.x,
                    item.y,
                    item.x+item.width,
                    item.y+item.height))
            else:
                print('you failed at math! %s %s' % (item.x, item.y))
