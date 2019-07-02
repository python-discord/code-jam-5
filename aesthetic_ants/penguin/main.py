import pyglet
from .enemy import Enemy

window = pyglet.window.Window(caption='Penguin Snowball')
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

enemy = Enemy()


@window.event
def on_draw():
    window.clear()
    enemy.draw()


def main():
    pyglet.clock.schedule_interval(enemy.update, 1/120)
    pyglet.app.run()


if __name__ == '__main__':
    main()
