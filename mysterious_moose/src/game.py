import src.graphics as graphics
import src.blocks as blocks


class Game:
    def __init__(self, graphics):
        self.graphics = graphics
        self.blocks = blocks.get_blocks()

    def update(self):
        """ called each loop to update the game """
        pass
