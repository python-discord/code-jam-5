from . import keys
from . import player, zone_map
from config import current_zone
import pyglet

def handle_input():
    # print('old player: %s %s' % (player.x, player.y))
    new_x = player.x
    new_y = player.y
    if pyglet.window.key.UP in keys:
        new_y += 1
    if pyglet.window.key.DOWN in keys:
        new_y -= 1
    if pyglet.window.key.LEFT in keys:
        new_x -= 1
    if pyglet.window.key.RIGHT in keys:
        new_x += 1
    permitted = checkCollision(new_x, new_y)
    if permitted:
        player.x = new_x
        player.y = new_y
        # print('new player: %s, %s' % (player.x, player.y))

def checkCollision(new_x, new_y):
    query_x = -1024 + (new_x * player.width)
    query_y = -1024 + (new_y * player.height)
    # print('queried %s,%s' % (query_x, query_y))
    zone_query = zone_map[current_zone].index.intersect(
        bbox=(query_x, query_y, query_x, query_y))
    for i in zone_query:
        print('found:%s which is %s' % (i.name, i.collision))
        if i.collision:
            permitted = False
            return False
    return True
