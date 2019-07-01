import pyglet
from config import *
from . import game_window
from . import zone_map
from . import time_display
from . import player

def render_loop():
    '''
    This contains the logic for the main render loop

    As Pyglet only uses a single function for the render loop, that function
    can get pretty large, and really deserves its own file.

    Usage: Import it normally, and call like this:

    window = pyglet.window.Window()
    window.push_handlers(on_draw=render_loop)
    '''

    label = pyglet.text.Label('player x %s y %s zone %s' % (player.x, player.y, current_zone),
                              font_name='Times New Roman',
                              font_size=16,
                              x=game_window.width//3, y=24, color=(0, 0, 0, 255))
    # blank screen!
    game_window.clear()

    # batch up all zone drawing
    batch = pyglet.graphics.Batch()
    for i in zone_map[current_zone].index.intersect(bbox=(
            player.x-view_distance-player.center_x,
            player.y-view_distance-player.center_y,
            player.x+view_distance-player.center_x,
            player.y+view_distance-player.center_y)):
        batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', (
            i.x + player.x, i.y + player.y,
            i.x+i.width + player.x, i.y + player.y,
            i.x + i.width + player.x, i.y + i.height + player.y,
            i.x + player.x, i.y + i.width + player.y)),
         ('c3B', i.color))
        pyglet.text.Label(i.name, batch=batch, x=i.x+5+player.x, y=i.y+5+player.y)
    batch.draw()

    # draw player fixed (static center)
    x = player.center_x
    y = player.center_y
    quad = pyglet.graphics.vertex_list(4,
                                       ('v2i', (x, y,
                                                x, y+player.height,
                                                x + player.width, y + player.height,
                                                x+player.width, y)),
                                       ('c3B', (0, 0, 255,
                                                0, 0, 255,
                                                0, 0, 255,
                                                0, 255, 255)))
    quad.draw(pyglet.gl.GL_QUADS)
    player_label = pyglet.text.Label(player.name, x=x, y=y, color=(255, 0, 0, 255))
    player_label.draw()

    # UI / debug elements
    label.draw()
    time_display.draw()
