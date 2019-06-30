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

    # Variables to handle tile transformation
    max_scale: float = 1.5
    current_scale: float = 1
    breathing_speed: float = 0.025  # how much to scale on each game tick
    breathing_direction: int = 1  # 1 -> outwards, -1 -> inwards

    def __init__(self, image: str):
        self.__image = load(image).convert_alpha()

        scale_percent = TILE_WIDTH / self.__image.get_width()
        new_height = int(self.__image.get_height() * scale_percent)

        # scale image based on game screen size
        self.__image = scale(self.__image, (TILE_WIDTH, new_height))

    def update(self) -> None:
        """Update is called every game tick."""
        self.__breathe()

    def get_image(self) -> pg.Surface:
        """
        Returns image of this tile.

        Method transforms the image based on if it is a task or not.
        """
        transformed_image = self.__image

        # Scaled based on original image
        new_width = int(self.__image.get_width() * self.current_scale)
        new_height = int(self.__image.get_height() * self.current_scale)
        transformed_image = scale(transformed_image, (new_width, new_height))
        if self.has_task:
            # Add colored tint
            transformed_image.fill((255, 0, 0, 150), special_flags=pg.BLEND_MULT)

        return transformed_image

    def __breathe(self) -> None:
        """Will add "breathing" effect to the tile if it has a task active."""
        if self.has_task:
            # Limit scale
            if self.current_scale >= self.max_scale:
                self.breathing_direction = -1
            elif self.current_scale <= 1:
                self.breathing_direction = 1

            self.current_scale += self.breathing_speed * self.breathing_direction
