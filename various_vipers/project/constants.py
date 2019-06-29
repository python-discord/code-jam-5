"""All game contstants."""
import logging

from pathlib import PurePath


FPS = 60

WIDTH = 1280
HEIGHT = 720

LOG_LEVEL = logging.DEBUG

# How many pixels the background is allowed to move in 1 game tick
BG_SCROLL_SPEED = 10


class Color:
    """Represent RGB color values."""

    black = (0, 0, 0)

    white = (255, 255, 255)

    red = (255, 0, 0)

    aqua = (0, 255, 255)


class Button:
    """Represents buttons properties."""

    main_btn_w = 400
    main_btn_h = 100
    btn_gap = 50


PATH_PROJECT = PurePath(__file__).parent

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")
PATH_BUTTONS = PurePath(PATH_PROJECT).joinpath("assets/images/buttons")

# Game assets

# Background images
GAME_BG_DESERT = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorDesert.png")
GAME_BG_FALL = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorFall.png")
GAME_BG_FOREST = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorForest.png")
GAME_BG_GRASS = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorGrass.png")


# UI assets

# Button images
PLAY_BTN = PurePath(PATH_BUTTONS).joinpath("play-btn-test.png")
PLAY_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("play-btn-test-hover.png")

OPT_BTN = PurePath(PATH_BUTTONS).joinpath("opt-btn-test.png")
OPT_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("opt-btn-test-hover.png")

QUIT_BTN = PurePath(PATH_BUTTONS).joinpath("quit-btn-test.png")
QUIT_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("quit-btn-test-hover.png")
