import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import TILE_WIDTH


class Tile:
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    image: pg.image = None

    def __init__(self, image: str):
        self.image = load(image)
        # scale image based on game screen size
        self.image = scale(self.image, (TILE_WIDTH, TILE_WIDTH))
