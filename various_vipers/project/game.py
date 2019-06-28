import pygame as pg

from project.constants import WIDTH, HEIGHT, FPS, Color


class Game:
    """
    Represents main game class
    """
    def __init__(self):
        pg.init()
        pg.display.set_caption('Various Vipers game in development')

        self.running = True

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

    def run(self):
        self.clock.tick(FPS)
        self._get_events()
        self._draw()

    def _get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        self.screen.fill(Color.black)
        pg.display.flip()
