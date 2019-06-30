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
                              font_size=12,
                              x=game_window.width//2, y=game_window.height//2, anchor_x='right', anchor_y='bottom')
    game_window.clear()
    for i in zone_map[current_zone].index.intersect(bbox=(
            player.x-view_distance,
            player.y-view_distance,
            player.x+view_distance,
            player.y+view_distance)):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', [
            i.x, i.y, i.x+i.width, i.y,
            i.x + i.width, i.y + i.height, i.x, i.y + i.width])
                             )
    #draw player
    quad = pyglet.graphics.vertex_list(4,
                                       ('v2i', (10, 10, 100, 10, 100, 100, 10, 100)),
                                       ('c3B', (0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 255, 0)))
    quad.draw(pyglet.gl.GL_QUADS)
#    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', [
#        player.x, player.y,
#        player.x + player.width, player.y,
#        player.x + player.width, player.y + player.height,
#        player.x, player.y + player.width]))

    label.draw()
    time_display.draw()
