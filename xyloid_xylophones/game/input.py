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

    new_move= allowed_move(new_x, new_y)
    move(new_move[0], new_move[1])

def move(new_x, new_y):
    '''Changes players position'''
    player.x = new_x
    player.y = new_y

def allowed_move(new_x, new_y):
    '''Returns the position that the player is allowed to move to'''
    x_collide = check_collision(new_x, player.y)
    y_collide = check_collision(player.x, new_y)
    both_collide = check_collision(new_x, new_y)
    if both_collide and x_collide and y_collide:
        #Player is allowed to move to new position
        return [new_x, new_y]
    elif x_collide:
        #Player is allowed to move on x-axis
        return [new_x, player.y]
    elif y_collide:
        #Player is allowed to move on y-axis
        return [player.x, new_y]

    return [player.x, player.y] #Player cannot move

def check_collision(new_x, new_y):
    '''Verifies that the character is allowed to move to this position. Returns True if user can move to position'''
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
