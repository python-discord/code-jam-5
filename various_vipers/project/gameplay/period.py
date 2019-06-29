from .earth import Earth

from project.constants import (
    GAME_BG_DESERT,
    GAME_BG_FALL,
    GAME_BG_FOREST,
    GAME_BG_GRASS,
)


class Period(object):
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
        self.earth.update()

    def draw(self):
        self.earth.draw()


class PeriodMedieval(Period):
    pass


class PeriodModern(Period):
    pass


class PeriodFuture(Period):
    pass
