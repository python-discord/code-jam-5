"""All game contstants."""

import logging
from pathlib import Path, PurePath


LOG_LEVEL = logging.DEBUG

FPS = 60

WIDTH = 1285
HEIGHT = 725

# Biomes are transformed to squares
# Width of a single biome (biomes can be chained together)
BIOME_WIDTH: int = 600
# Tile height is scaled based on how much the width scaled
# Width of a single tile (BIOME_WIDTH should be divisable by TILE_WIDTH)
TILE_WIDTH: int = 75
# Number of tile columns per biome
TILE_COLS: int = int(BIOME_WIDTH // TILE_WIDTH)
# Number of tile rows per biome
TILE_ROWS: int = 4

# How many pixels the background is allowed to move in 1 game tick
BG_SCROLL_SPEED = 20


class Color:
    """Represent RGB color values."""

    black = (0, 0, 0)

    white = (255, 255, 255)

    red = (255, 0, 0)

    aqua = (0, 255, 255)

    sky = (207, 239, 252)


class WindowState:
    """Represents windows states."""

    game = "game"
    main_menu = "main_menu"
    options = "options"
    quited = "quit"


class Button:
    """Represents buttons properties."""

    main_btn_w = 400
    main_btn_h = 100
    btn_gap = 50


PATH_PROJECT = PurePath(__file__).parent

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")
PATH_TILES = PurePath(PATH_PROJECT).joinpath("assets/images/tiles")
PATH_BUTTONS = PurePath(PATH_PROJECT).joinpath("assets/images/buttons")

# Game assets

# Background images
GAME_BG_DESERT = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorDesert.png")
GAME_BG_FALL = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorFall.png")
GAME_BG_FOREST = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorForest.png")
GAME_BG_GRASS = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorGrass.png")

# Tiles

TILES_GRASS = list(Path(PATH_TILES).joinpath("grass").glob("*"))
TILES_WATER = list(Path(PATH_TILES).joinpath("water").glob("*"))

# UI assets

# Button images
PLAY_BTN = PurePath(PATH_BUTTONS).joinpath("play-btn-test.png")
PLAY_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("play-btn-test-hover.png")

OPT_BTN = PurePath(PATH_BUTTONS).joinpath("opt-btn-test.png")
OPT_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("opt-btn-test-hover.png")

QUIT_BTN = PurePath(PATH_BUTTONS).joinpath("quit-btn-test.png")
QUIT_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("quit-btn-test-hover.png")

BACK_BTN = PurePath(PATH_BUTTONS).joinpath("back-btn-test.png")
BACK_BTN_HOVER = PurePath(PATH_BUTTONS).joinpath("back-btn-test-hover.png")
