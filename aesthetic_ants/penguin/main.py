import pyglet

from .player import Player
from .utils import keys

window = pyglet.window.Window(caption='Penguin Snowball')

player = Player(window.width / 2, window.height / 2)


@window.event
def on_draw():
    window.clear()
    player.draw()


def main():
    window.push_handlers(player)  # Registers the player event handler
    window.push_handlers(keys)  # Register the utility keyboard handler
    pyglet.app.run()


if __name__ == '__main__':
    main()
