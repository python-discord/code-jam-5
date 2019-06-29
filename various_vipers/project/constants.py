import logging

from pathlib import PurePath


FPS = 60

WIDTH = 1200
HEIGHT = 800

LOG_LEVEL = logging.DEBUG


class Color:
    black = (0, 0, 0)


PATH_PROJECT = PurePath(__file__).parent

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")

# Game assets

# Background images
GAME_BG_IMAGES = [
    PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorDesert.png"),
    PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorFall.png"),
    PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorForest.png"),
    PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorGrass.png"),
]
