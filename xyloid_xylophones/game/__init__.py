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
# static center of player square
player.center_x = 4*64
player.center_y = 4*64
# center of all the squares aka 0,0
player.x = zone_width // 2
player.y = zone_height // 2
player.width = sprite_width
player.height = sprite_height

for i in zone_names:
    for y in range(0, zone_height):
        for x in range(0, zone_width):
            item = Item('x%sy%s' % (x, y))
            item.y = -1024 + (y * sprite_height)
            item.x = -1024 + (x * sprite_width)
            # tiny offset for grid view
            item.width = sprite_width-1
            item.height = sprite_height-1
            # boarder is not passable
            if (y == player.x) & (x == player.y):
                item.Collision = False
            elif (
                    (y == 0) or
                    (x == 0) or
                    (y == zone_height-1) or
                    (x == zone_width-1)
            ):
                item.collision = True
            else:
                item.collision = not getrandbits(1)
            # if collision draw as red
            if item.collision:
                item.color = (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)
            else:
                # otherwise draw as green
                item.color = (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)
            # double check we didn't create more then one in a square
            if not zone_map[i].index.intersect(bbox=(item.x,
                                                     item.y,
                                                     item.x + item.width,
                                                     item.y + item.height)):
                # print('created x%sy%s(%s,%s)' % (x, y, item.x, item.y))
                zone_map[i].index.insert(item, bbox=(
                    item.x,
                    item.y,
                    item.x+item.width,
                    item.y+item.height))
            else:
                print('you failed at math! %s %s' % (item.x, item.y))
