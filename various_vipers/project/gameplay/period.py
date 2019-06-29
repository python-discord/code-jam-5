from project.constants import (
    GAME_BG_DESERT,
    GAME_BG_FALL,
    GAME_BG_FOREST,
    GAME_BG_GRASS,
)
from .earth import Earth


class Period(object):
    """
    This class represents an abstract Time Period Style.

    Game difficulties are split into Time Periods - with each time period having different
      tile styles, tasks, images and chances to spawn cities.
    """

    # List of background images, that will be looped through
    background_images = [
        GAME_BG_DESERT,
        GAME_BG_DESERT,
        GAME_BG_DESERT,
        GAME_BG_FALL,
        GAME_BG_FALL,
        GAME_BG_FALL,
        GAME_BG_FOREST,
        GAME_BG_FOREST,
        GAME_BG_FOREST,
        GAME_BG_GRASS,
        GAME_BG_GRASS,
        GAME_BG_GRASS,
    ]
    # Map of tiles for current period
    earth_tilemap = [[], [], [], []]

    def __init__(self, screen):
        self.screen = screen
        self.earth = Earth(self.screen, self.background_images, self.earth_tilemap)

    def update(self):
        """Update gets called every game tick."""
        self.earth.update()

    def draw(self):
        """Draw gets called every game tick."""
        self.earth.draw()


class PeriodMedieval(Period):
    """Medieval themed Time Period."""

    pass


class PeriodModern(Period):
    """Modern time themed Time Period."""

    pass


class PeriodFuture(Period):
    """Future time themed Time Period."""

    pass
