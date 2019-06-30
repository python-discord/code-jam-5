import pyglet
from config import *

from .render_loop import render_loop
from . import game_window
from . import player

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
    if symbol == pyglet.window.key.UP:
        player.y -= player_step
    if symbol == pyglet.window.key.DOWN:
        player.y += player_step
    if symbol == pyglet.window.key.LEFT:
        player.x -= player_step
    if symbol == pyglet.window.key.RIGHT:
        player.x += player_step
    keys.add(symbol)


@game_window.event
def on_key_release(symbol, modifiers):
    '''
    Handle keyreleases

    The inverse of `on_key_press`, this removes `symbol` from `keys`.
    '''
    print(symbol)
    if symbol in keys:  # print screen does not make it into keys set
        keys.remove(symbol)


if __name__ == '__main__':
    pyglet.app.run()
