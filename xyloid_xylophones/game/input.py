'''Handles all user input from keyboard and mouse'''
import pyglet
from config import game_width, game_height
from . import keys, player, zone_map, current_display



def mouse_input(x, y):
    if (current_display == 'zone'):
        move_towards_coord(x, y, True)
    else:
        # TODO
        pass
    return


def move_towards_coord(x, y, from_mouse=False):
    action = None
    """Moves the player towards the (x,y) coordinate"""
    # Get center of the screen
    x_mid = game_width / 2
    y_mid = game_height / 2

    new_x = player.x
    new_y = player.y

    if (x > (x_mid + player.width / 2)) or (x < (x_mid - player.width / 2)):
        # if mouse click is outside of the width of the player
        if x > x_mid:
            new_x += 1
            player.update_sprite("right")
        elif x < x_mid:
            new_x -= 1
            player.update_sprite("left")
    if (y > (y_mid + player.height / 2)) or (y < (y_mid - player.height / 2)):
        # if mouse click is outside the height of the player
        if y > y_mid:
            new_y += 1
            player.update_sprite("up")
        elif y < y_mid:
            new_y -= 1
            player.update_sprite("down")
    if from_mouse:
        action = check_action(new_x, new_y)

    new_move = allowed_move(new_x, new_y)
    move(new_move[0], new_move[1], action)  # Move towards the new point


def handle_input(dt=None):
    action = None
    """Moves the player to a new position if allowed"""
    if len(keys) > 0:
        new_x = player.x
        new_y = player.y
        if pyglet.window.key.UP in keys:
            new_y += 1
            player.update_sprite("up")
        if pyglet.window.key.DOWN in keys:
            new_y -= 1
            player.update_sprite("down")
        if pyglet.window.key.LEFT in keys:
            new_x -= 1
            player.update_sprite("left")
        if pyglet.window.key.RIGHT in keys:
            new_x += 1
            player.update_sprite("right")
        if pyglet.window.key.ENTER in keys:
            action = check_action(new_x, new_y)
        elif pyglet.window.key.SPACE in keys:
            action = check_action(new_x, new_y)

        if (new_x != player.x) | (new_y != player.y):
            new_move = allowed_move(new_x, new_y)
            if (new_move[0] != player.x) | (new_y != player.y):
                move(new_move[0], new_move[1], action)
    else:
        pass
        # player.update_sprite()


def move(new_x, new_y, action=None):
    """Changes players position"""
    player.x = new_x
    player.y = new_y
    player.action = action


def allowed_move(new_x, new_y):
    """Returns the position that the player is allowed to move to"""
    x_collide = check_collision(new_x, player.y)
    y_collide = check_collision(player.x, new_y)
    both_collide = check_collision(new_x, new_y)
    if both_collide and x_collide and y_collide:
        # Player is allowed to move to new position
        return [new_x, new_y]
    elif x_collide:
        # Player is allowed to move on x-axis
        return [new_x, player.y]
    elif y_collide:
        # Player is allowed to move on y-axis
        return [player.x, new_y]

    return [player.x, player.y]  # Player cannot move


def check_collision(new_x, new_y):
    """
    Verifies that the character is allowed to move to this position.
    Returns True if user can move to position
    """
    query_x = -1024 + (new_x * player.width)
    query_y = -1024 + (new_y * player.height)
    # print('queried %s,%s' % (query_x, query_y))
    zone_query = zone_map[player.current_zone].index.intersect(
        bbox=(query_x, query_y, query_x, query_y)
    )
    for i in zone_query:
        # print('found:%s which is %s' % (i.name, i.collision))
        if i.collision:
            return False
    return True


def check_action(new_x, new_y):
    """
    confirm the next block has an action
    Returns action string
    """
    query_x = -1024 + (new_x * player.width)
    query_y = -1024 + (new_y * player.height)
    # print('queried %s,%s' % (query_x, query_y))
    zone_query = zone_map[player.current_zone].index.intersect(
        bbox=(query_x, query_y, query_x, query_y)
    )
    for i in zone_query:
        # print('found:%s which is %s' % (i.name, i.collision))
        if i.contains != 'default_nothing':
            return i.contains
        else:
            return None
    return None
