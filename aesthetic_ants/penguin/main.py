import pyglet
from .enemy import Enemy

from .player import Player
from .utils import keys

window = pyglet.window.Window(caption='Penguin Snowball')
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player = Player(window.width / 2, window.height / 2)
enemy = Enemy()


@window.event
def on_draw():
    window.clear()
    player.draw()
    enemy.draw()


def update(dt):
    player.update(dt)
    enemy.update(dt)


def main():
    window.push_handlers(player)  # Registers the player event handler
    window.push_handlers(keys)  # Register the utility keyboard handler
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()


if __name__ == '__main__':
    main()
