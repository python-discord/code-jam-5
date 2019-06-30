import pyglet
from enemy import Enemy

window = pyglet.window.Window(caption='Penguin Snowball')
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()
enemy_image = pyglet.resource.image('circle.png')
enemy_image.width = 50
enemy_image.height = 50


enemy = Enemy(enemy_image)


def main():
    pyglet.clock.schedule_interval(enemy.update, 1/120)
    pyglet.app.run()


@window.event
def on_draw():
    window.clear()
    enemy.draw()


if __name__ == '__main__':
    main()
