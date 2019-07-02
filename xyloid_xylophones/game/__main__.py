import pyglet
from config import *
from os import listdir
from os.path import isfile, join, isdir, basename, splitext
from pathlib import Path

from .render_loop import render_loop
from . import game_window, player, zone_map, Item, sound_list, music_list, cut_scenes
from random import getrandbits

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
    for i in zone_map[current_zone].index.intersect(bbox=(query_x, query_y, query_x, query_y)):
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
    cut_scenes = load_list(location_scenes)
    sound_list = load_list(location_sound)
    music_list = load_list(location_music)
    generate_random_zones()
    pyglet.app.run()
