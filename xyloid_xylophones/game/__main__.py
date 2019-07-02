import pyglet
from config import *
from os import listdir
from os.path import isfile, join, isdir, basename, splitext
from pathlib import Path

from .render_loop import render_loop
from . import game_window, player, zone_map, Item, sound_list, music_list, cut_scenes
from . import keys
from random import getrandbits
from .input import mouse_input

game_window.push_handlers(on_draw=render_loop)  # Set the render loop handler.


@game_window.event
def on_key_press(symbol, modifiers):
    '''
    Handle keypresses.

    This function is used to handle keypresses. Currently, this is accomplished
    by adding `symbol` to the `keys` set. `modifiers` is not used, but required
    for the function signature.
    '''
    keys.add(symbol)


@game_window.event
def on_key_release(symbol, modifiers):
    '''
    Handle keyreleases

    The inverse of `on_key_press`, this removes `symbol` from `keys`.
    '''

    if symbol in keys:  # print screen does not make it into keys set
        keys.remove(symbol)

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_input(x, y)

def generate_random_zones():
    '''
    populate zone_map with a random maze
    :return: None
    '''
    for i in zone_names:
        for y in range(0, zone_height):
            for x in range(0, zone_width):
                item = Item('x%sy%s' % (x, y))
                item.y = -1024 + (y * sprite_height)
                item.x = -1024 + (x * sprite_width)
                # tiny offset for grid view
                item.width = sprite_width - 1
                item.height = sprite_height - 1
                # boarder is not passable
                if (y == player.x) & (x == player.y):
                    item.Collision = False
                elif (y == 0) | (x == 0) | (y == zone_height - 1) | (x == zone_width - 1):
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
                        item.x + item.width,
                        item.y + item.height))
                # else:
                #     print('you failed at math! %s %s' % (item.x, item.y))


def load_list(abstract_path):
    '''
    get the list of files with short name
    :return: a list of idex by short file name to full_path + filename
    '''
    temp_list = {}
    result_list = {}
    fullpath = join(Path(__file__).resolve().parents[1], Path(abstract_path))
    if isdir(fullpath):
        temp_list = [f for f in listdir(fullpath) if isfile(join(fullpath, f))]
    for f in temp_list:
        i = splitext(basename(f))[0]
        result_list[i] = join(fullpath, f)
        print('%s %s' % (i, result_list[i]))
    return result_list


if __name__ == '__main__':
    #cut_scenes = load_list(location_scenes)
    #sound_list = load_list(location_sound)
    #music_list = load_list(location_music)
    generate_random_zones()
    pyglet.app.run()
