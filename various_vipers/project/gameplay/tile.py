import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import TILE_WIDTH


class Tile:
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    image: pg.Surface = None

    def __init__(self, image: str):
        self.image = load(image).convert_alpha()

        scale_percent = TILE_WIDTH / self.image.get_width()
        new_height = int(self.image.get_height() * scale_percent)

        # scale image based on game screen size
        self.image = scale(self.image, (TILE_WIDTH, new_height))
