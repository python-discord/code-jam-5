import pyglet
from config import *
from os import listdir
from os.path import isfile, join, isdir, basename, splitext, realpath, split
from pathlib import Path
from pyglet import gl
from pyglet.image.codecs.png import PNGImageDecoder

#from .render_loop import render_loop
from . import game_window, player, zone_map, Item, sound_list, music_list, scene_list, Resource, tick
from . import keys, time_display, elapsed_time, media, level1map
from .gamemap import Map
from random import getrandbits
from .input import mouse_input, handle_input


@game_window.event
def on_key_press(symbol, modifiers):
    '''
    Handle keypresses.

    This function is used to handle keypresses. Currently, this is accomplished
    by adding `symbol` to the `keys` set. `modifiers` is not used, but required
    for the function signature.
    '''

    keys.add(symbol)

    if len(keys) > 0:
        handle_input()


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
        resource = Resource()
        resource.full_path = join(fullpath, f)
        resource.stream = open(resource.full_path,'rb')
        if resource.full_path.endswith('.png'):
            resource.data = pyglet.image.load(i, file=resource.stream, decoder=PNGImageDecoder())
        elif resource.full_path.endswith('.wav'):
            resource.data = pyglet.media.load(resource.full_path)
        result_list[i] = resource
        print('%s %s' % (i, join(fullpath, f)))
    return result_list

def ticker(dt=None):
    global tick
    tick += 1

def render_loop():
    global cut_scene
    global elapsed_time
    global tick
    '''
    This contains the logic for the main render loop

    As Pyglet only uses a single function for the render loop, that function
    can get pretty large, and really deserves its own file.

    Usage: Import it normally, and call like this:

    window = pyglet.window.Window()
    window.push_handlers(on_draw=render_loop)
    '''

    # Set some OpenGL options to make things scale properly
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_MAG_FILTER,
        gl.GL_NEAREST)

    # blank screen!
    game_window.clear()
    if cut_scene:
        if elapsed_time < cut_scene_timeout:
            scene_list[cut_scene_name].data.blit(0, 0)
            elapsed_time = tick
            # add a fade @ a %?
        else:
            cut_scene = False
    else:
        level1map.draw()

        # draw player fixed (static center)
        x = player.center_x
        y = player.center_y
        quad = pyglet.graphics.vertex_list(
            4,
            ('v2i', (x, y,
                     x, y+player.height,
                     x + player.width, y + player.height,
                     x+player.width, y)),
            ('c3B', (0, 0, 255,
                     0, 0, 255,
                     0, 0, 255,
                     0, 255, 255)))
        quad.draw(pyglet.gl.GL_QUADS)
        player_label = pyglet.text.Label(
            player.name, x=x, y=y, color=(255, 0, 0, 255))
        player_label.draw()

    # UI / debug elements
    label = pyglet.text.Label(
        'player x %s y %s zone %s' % (player.x, player.y, current_zone),
        font_name='Times New Roman',
        font_size=16,
        x=game_window.width//3, y=24, color=(0, 0, 0, 255))
    label.draw()
    time_display.draw()

if __name__ == '__main__':
    game_window.push_handlers(on_draw=render_loop)  # Set the render loop handler.

    pyglet.clock.schedule(lambda dt: None)

    scene_list = load_list(location_scene)
    # sound_list = load_list(location_sound)

    generate_random_zones()
    player.load_player()

    pyglet.clock.schedule_interval(handle_input, 0.15)
    pyglet.clock.schedule_interval(ticker, 0.33)

    pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
    pyglet.options['search_local_libs'] = True

    music_list = load_list(location_music)

    # looper = pyglet.media.SourceGroup(music_list['default'].data.audio_format, None)
    # looper.loop = True
    # looper.queue(music_list['default'].data)
    #media.queue(music_list['default'].data)
    #media.volume = 0.05
    #media.play()
    pyglet.app.run()
