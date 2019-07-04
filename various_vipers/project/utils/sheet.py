import pygame as pg


class Sheet:
    """Represents tool for extracting images from spritesheet."""

    def __init__(self, sheet_path):
        self.spritesheet = pg.image.load(sheet_path).convert_alpha()

    def get_image(self, x, y, width, height, alpha=False):
        """
        Extracts sprite of given point (x, y) (left, top) and width and height.

        Alpha boolean keyword argument for converting the sprite in alpha or non-alpha.
        """
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        image.set_alpha(255)

        if alpha:
            return image.convert_alpha()
        return image.convert()
