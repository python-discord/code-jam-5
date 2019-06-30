import pyglet

from . import game_window


def render_loop():
    '''
    This contains the logic for the main render loop

    As Pyglet only uses a single function for the render loop, that function
    can get pretty large, and really deserves its own file.

    Usage: Import it normally, and call like this:

    window = pyglet.window.Window()
    window.push_handlers(on_draw=render_loop)
    '''

    label = pyglet.text.Label('Hello, world',
                              font_name='Times New Roman',
                              font_size=36,
                              x=game_window.width//2, y=game_window.height//2,
                              anchor_x='center', anchor_y='center')
    game_window.clear()
    label.draw()
