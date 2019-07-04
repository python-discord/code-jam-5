import pyglet
from game_modules.start_menu import make_gui

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

start_window = pyglet.window.Window()

gui = make_gui(start_window)

pyglet.app.run()
