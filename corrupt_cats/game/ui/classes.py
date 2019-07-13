import arcade


class NSprite(arcade.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.args = args

    @property
    def center(self):
        return self.center_x, self.center_y

    @property
    def size(self):
        return self.width, self.height

    def copy(self):
        return NSprite(*self.args)
