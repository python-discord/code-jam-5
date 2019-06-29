import pygame as pg
from pygame.image import load


class Tile:
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    bg_image: pg.image = None

    def __init__(self, image: str):
        self.bg_image = load(image)
