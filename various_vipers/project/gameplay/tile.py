import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import TILE_WIDTH


class Tile:
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    __image: pg.Surface = None

    # Boolean to check if this tile has a task to do
    # Tiles with tasks have different appearance
    has_task: bool = False

    def __init__(self, image: str):
        self.__image = load(image).convert_alpha()

        scale_percent = TILE_WIDTH / self.__image.get_width()
        new_height = int(self.__image.get_height() * scale_percent)

        # scale image based on game screen size
        self.__image = scale(self.__image, (TILE_WIDTH, new_height))

    def get_image(self):
        """
        Returns image of this tile.

        Method transforms the image based on if it is a task or not.
        """
        transformed_image = self.__image
        if self.has_task:
            new_width = int(transformed_image.get_width() * 1.3)
            new_height = int(transformed_image.get_height() * 1.3)
            transformed_image = scale(transformed_image, (new_width, new_height))
            transformed_image.fill((255, 0, 0, 150), special_flags=pg.BLEND_MULT)
        return transformed_image
