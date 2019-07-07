import pyglet
from config import *
from os import listdir
from os.path import isfile, join, isdir, basename, splitext, realpath, split
from pathlib import Path
from pyglet import gl
from pyglet.image.codecs.png import PNGImageDecoder
from math import floor
from . import game_window, player, zone_map, Item, sound_list, music_list, scene_list, Resource, elapsed_time, keys, \
    time_display, media, level_map, level_key, tick
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


def load_zones(file_name):
    '''
    load the map file
    :return: None
    '''
    t = [[]]
    i = 0
    with open(file_name, 'rb') as f:
        key = f.read(1)
        while key != b'':
            ikey = int.from_bytes(key, 'big')
            if ikey > 0:
                t[i].append(ikey)
            else:
                i += 1
                t.append([])
            key = f.read(1)
    map_size = i

    for i in zone_names:
        for y in range(0, zone_height):
            for x in range(0, zone_width):
                item = Item('x%sy%s' % (x, y))
                item.y = -1024 + (y * sprite_height)
                item.x = -1024 + (x * sprite_width)
                item.sprite = t[(map_size-1) - (y - (floor(y / map_size) * map_size))][x - (floor(x / map_size) * map_size)]
                # tiny offset for grid view
                item.width = sprite_width - 1
                item.height = sprite_height - 1
                # boarder is not passable
                if (y == player.x) & (x == player.y):
                    item.Collision = False
                elif (y == 0) | (x == 0) | (y == zone_height - 1) | (x == zone_width - 1):
                    item.collision = True
                else:
                    item.collision = level_key[item.sprite]  # not getrandbits(1)
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
        resource.stream = open(resource.full_path, 'rb')
        if resource.full_path.endswith('.png'):
            resource.data = pyglet.image.load(i, file=resource.stream, decoder=PNGImageDecoder())
        elif resource.full_path.endswith('.ogg'):
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
        # level1map.draw()
        batch = pyglet.graphics.Batch()
        sprites = []
        offset_x = -1024 + ((4 + (zone_width - (player.x))) * sprite_width)
        offset_y = -1024 + ((4 + (zone_height - player.y)) * sprite_height)
        for i in zone_map[current_zone].index.intersect(bbox=(
                -1024 + ((player.x - view_distance) * sprite_width),
                -1024 + ((player.y - view_distance) * sprite_height),
                -1024 + ((player.x + view_distance) * sprite_width),
                -1024 + ((player.y + view_distance) * sprite_height))):
            sprites.append(pyglet.sprite.Sprite(level_map[i.sprite],
                                                i.x + offset_x, i.y + offset_y,
                                                batch=batch))
        batch.draw()
        # draw player fixed (static center)
        player.sprite.draw()  # Draw the player
        player.adjustment = 0
        x = player.center_x
        y = player.center_y
        player_label = pyglet.text.Label(
            player.name, x=x, y=y, color=(255, 0, 0, 255))
        player_label.draw()

    # UI / debug elements
    label = pyglet.text.Label(
        'player x %s y %s zone %s' % (player.x, player.y, current_zone),
        font_name='Times New Roman',
        font_size=16,
        x=game_window.width // 3, y=24, color=(0, 0, 0, 255))
    label.draw()
    time_display.draw()


if __name__ == '__main__':
    game_window.push_handlers(on_draw=render_loop)  # Set the render loop handler.

    pyglet.clock.schedule(lambda dt: None)

    # populate level_map with sprites
    assets_path = split(realpath(__file__))[0] + '/../assets/'
    grid = pyglet.image.load(assets_path + 'sheet.png')
    level_map.append(None)
    level_map.append(grid.get_region(0, 0, 64, 64))
    level_map.append(grid.get_region(64, 0, 64, 64))
    level_map.append(grid.get_region(128, 0, 64, 64))
    level_map.append(grid.get_region(192, 0, 64, 64))
    level_map.append(grid.get_region(256, 0, 64, 64))
    level_map.append(grid.get_region(320, 0, 64, 64))
    level_map.append(grid.get_region(384, 0, 64, 64))
    level_map.append(grid.get_region(448, 0, 64, 64))
    level_map.append(grid.get_region(512, 0, 64, 64))
    level_map.append(grid.get_region(576, 0, 64, 64))
    level_map.append(grid.get_region(640, 0, 64, 64))
    level_map.append(grid.get_region(704, 0, 64, 64))
    level_map.append(grid.get_region(768, 0, 64, 64))
    level_map.append(grid.get_region(832, 0, 64, 64))
    level_map.append(grid.get_region(896, 0, 64, 64))
    level_map.append(grid.get_region(960, 0, 64, 64))
    level_map.append(grid.get_region(1024, 0, 64, 64))
    level_map.append(grid.get_region(1088, 0, 64, 64))
    level_map.append(grid.get_region(1152, 0, 64, 64))
    level_map.append(grid.get_region(1216, 0, 64, 64))

    scene_list = load_list(location_scene)
    sound_list = load_list(location_sound)

    load_zones(join(Path(__file__).resolve().parents[1], Path('assets/myfile.map')))
    player.load_player()

    pyglet.clock.schedule_interval(handle_input, 0.15)
    pyglet.clock.schedule_interval(ticker, 0.33)

    music_list = load_list(location_music)

    # looper = pyglet.media.SourceGroup(music_list['default'].data.audio_format, None)
    # looper.loop = True
    # looper.queue(music_list['default'].data)
    media.queue(music_list['default'].data)
    # media.volume = 0.05
    media.play()
    pyglet.app.run()
