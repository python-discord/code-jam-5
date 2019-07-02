from . import keys
from . import player, zone_map
from config import current_zone
import pyglet

def handle_input():
    '''Moves the player to a new position if allowed'''
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

    if checkCollision(new_x, new_y):
        move(new_x, new_y) #Player moves to the new position
    elif checkCollision(player.x, new_y):
        move(player.x, new_y) #Player collided with something on the x-axis
    elif checkCollision(new_x, player.y):
        move(new_x, player.y) #Player collided with something on y-axis

def move(new_x, new_y):
    '''Changes players position'''
    player.x = new_x
    player.y = new_y

def checkCollision(new_x, new_y):
    '''Verifies that the character is allowed to move to this position'''
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
