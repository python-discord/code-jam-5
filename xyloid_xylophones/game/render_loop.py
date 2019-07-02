import pyglet
from pyglet import gl

from config import *
from . import game_window
from . import zone_map
from . import time_display
from . import player
from .input import handle_input

def render_loop():
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

#    label = pyglet.text.Label(
#        'player x %s y %s zone %s' % (player.x, player.y, current_zone),
#        font_name='Times New Roman',
#        font_size=16,
#        x=game_window.width//3, y=24, color=(0, 0, 0, 255))

    # blank screen!
    game_window.clear()
    if cut_scene:
        print('cut')

    else:
        # batch up all zone drawing
        batch = pyglet.graphics.Batch()
        offset_x = -1024 + ((4+(zone_width-player.x)) * sprite_width)
        offset_y = -1024 + ((4+(zone_height-player.y)) * sprite_height)
        for i in zone_map[current_zone].index.intersect(bbox=(
                -1024+((player.x-view_distance)*sprite_width),
                -1024+((player.y-view_distance)*sprite_height),
                -1024+((player.x+view_distance)*sprite_width),
                -1024+((player.y+view_distance)*sprite_height))):
            batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', (
                i.x + offset_x, i.y + offset_y,
                i.x+i.width + offset_x, i.y + offset_y,
                i.x + i.width + offset_x, i.y + i.height + offset_y,
                i.x + offset_x, i.y + i.width + offset_y)),
             ('c3B', i.color))
#            pyglet.text.Label(
#                i.name,
#                batch=batch,
#                x=i.x + offset_x + 5,
#                y=i.y + offset_y + 5)
        batch.draw()

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
        handle_input()

    # UI / debug elements
#    label.draw()
    time_display.draw()
