"""All game contstants."""
import logging

from pathlib import PurePath


FPS = 60

WIDTH = 1280
HEIGHT = 720

LOG_LEVEL = logging.DEBUG

# How many pixels the background is allowed to move in 1 game tick
BG_SCROLL_SPEED = 20


class Color:
    """Represent RGB color value."""

    black = (0, 0, 0)

    white = (255, 255, 255)

    red = (255, 0, 0)

    sky = (207, 239, 252)


PATH_PROJECT = PurePath(__file__).parent

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")

# Game assets

# Background images
GAME_BG_DESERT = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorDesert.png")
GAME_BG_FALL = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorFall.png")
GAME_BG_FOREST = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorForest.png")
GAME_BG_GRASS = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorGrass.png")
