import pyglet
from player import Player

window = pyglet.window.Window(caption='Penguin Snowball')

player = Player(window.width / 2, window.height / 2)


@window.event
def on_draw():
    window.clear()
    player.draw()


def main():
    window.event(player.on_mouse_motion)  # Registers the player-mouse event handler
    pyglet.app.run()


if __name__ == '__main__':
    main()
