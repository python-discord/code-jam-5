import pyglet
import random as rand

class Enemy(pyglet.sprite.Sprite):

    def __init__(self, enemy_image):
        pyglet.sprite.Sprite.__init__(self, enemy_image)
        self.velocity_x, self.velocity_y = rand.randint(0, 100), rand.randint(0, 100)

    #def update(self):
         #enemy_image.x = 10
         #enemy_image.draw(self)


    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

