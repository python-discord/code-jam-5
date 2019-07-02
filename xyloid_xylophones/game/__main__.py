import pyglet
from config import *

from .render_loop import render_loop
from . import game_window
from . import player
from . import zone_map

game_window.push_handlers(on_draw=render_loop)  # Set the render loop handler.

# A set of pyglet.window.key symbols. Used for handling keypresses.
keys = set()


@game_window.event
def on_key_press(symbol, modifiers):
    '''
    Handle keypresses.

    This function is used to handle keypresses. Currently, this is accomplished
    by adding `symbol` to the `keys` set. `modifiers` is not used, but required
    for the function signature.
    '''
    # print('old player: %s %s' % (player.x, player.y))
    new_x = player.x
    new_y = player.y
    if symbol == pyglet.window.key.UP:
        new_y += 1
    if symbol == pyglet.window.key.DOWN:
        new_y -= 1
    if symbol == pyglet.window.key.LEFT:
        new_x -= 1
    if symbol == pyglet.window.key.RIGHT:
        new_x += 1
    permitted = True
    query_x = -1024 + (new_x * sprite_width)
    query_y = -1024 + (new_y * sprite_height)
    # print('queried %s,%s' % (query_x, query_y))
    zone_query = zone_map[current_zone].index.intersect(
        bbox=(query_x, query_y, query_x, query_y))
    for i in zone_query:
        print('found:%s which is %s' % (i.name, i.collision))
        if i.collision:
            permitted = False
            break
    if permitted:
        player.x = new_x
        player.y = new_y
        # print('new player: %s, %s' % (player.x, player.y))
    keys.add(symbol)


@game_window.event
def on_key_release(symbol, modifiers):
    '''
    Handle keyreleases

    The inverse of `on_key_press`, this removes `symbol` from `keys`.
    '''
    if symbol in keys:  # print screen does not make it into keys set
        keys.remove(symbol)


if __name__ == '__main__':
    pyglet.app.run()
