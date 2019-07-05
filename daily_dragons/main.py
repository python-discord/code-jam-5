import pyglet
from game_modules.start_menu import make_gui


start_window = pyglet.window.Window()

gui = make_gui(start_window)

pyglet.app.run()
