"""All game contstants."""
# flake8: noqa

import logging
from os import listdir
from pathlib import Path, PurePath


LOG_LEVEL = logging.DEBUG

FPS = 60

WIDTH = 960
HEIGHT = 720


# Biomes are transformed to squares
# Width of a single biome (biomes can be chained together)
BIOME_WIDTH: int = 480
# Tile height is scaled based on how much the width scaled
# Width of a single tile (BIOME_WIDTH should be divisable by TILE_WIDTH)
TILE_WIDTH: int = 60
# Number of tile columns per biome
TILE_COLS: int = int(BIOME_WIDTH // TILE_WIDTH)
# Number of tile rows per biome
TILE_ROWS: int = 4

# Sun constants
# Max heat before game over
MAX_HEAT: float = 100

INDICATOR_WIDTH: int = 100

# How many pixels the background is allowed to move in 1 game tick
BG_SCROLL_SPEED = 20
BG_CLOUDS_SCROLL_SPEED = 1
FG_CLOUDS_SCROLL_SPEED = 2

REPO_LINK = "https://github.com/skilldeliver/code-jam-5"


PATH_PROJECT = PurePath(__file__).parent

PATH_DATA = PurePath(PATH_PROJECT).joinpath("data")

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")
PATH_TILES = PurePath(PATH_PROJECT).joinpath("assets/images/tiles")
PATH_TASK = PurePath(PATH_PROJECT).joinpath("assets/images/task")
PATH_MAZE_TASK = PurePath(PATH_TASK).joinpath("maze")

PATH_BUTTONS = PurePath(PATH_PROJECT).joinpath("assets/images/UI/buttons")
PATH_SLIDER = PurePath(PATH_PROJECT).joinpath("assets/images/UI/slider")
PATH_UI_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/UI/backgrounds")
PATH_UI_AUDIO = PurePath(PATH_PROJECT).joinpath("assets/audio/UI")
PATH_MUSIC = PurePath(PATH_PROJECT).joinpath("assets/audio/music")
PATH_OTHER = PurePath(PATH_PROJECT).joinpath("assets/images/other")


USER_SETTINGS = PurePath(PATH_DATA).joinpath("user_settings.json")
# Game assets

# Background images
DESERT_BGS = list(Path(PATH_BACKGROUNDS).joinpath("desert").glob("*.png"))
CITY_BGS = list(Path(PATH_BACKGROUNDS).joinpath("city").glob("*.png"))
FOREST_BGS = list(Path(PATH_BACKGROUNDS).joinpath("forest").glob("*.png"))
MOUNTAINS_BGS = list(Path(PATH_BACKGROUNDS).joinpath("mountains").glob("*.png"))

# Background cloud layer will be behind foreground cloud layer
PATH_CLOUD_LAYERS = PurePath(PATH_BACKGROUNDS).joinpath("clouds/layers")
CLOUD_LAYERS_BG = [
    PurePath(PATH_CLOUD_LAYERS).joinpath("cloudLayer1.png"),
    PurePath(PATH_CLOUD_LAYERS).joinpath("cloudLayerB1.png"),
]
CLOUD_LAYERS_FG = [
    PurePath(PATH_CLOUD_LAYERS).joinpath("cloudLayer2.png"),
    PurePath(PATH_CLOUD_LAYERS).joinpath("cloudLayerB2.png"),
]

SUN_IMAGE = PurePath(PATH_OTHER).joinpath("sun.png")
INDICATOR_ARROW = PurePath(PATH_OTHER).joinpath("indicator.png")

# Tiles

TILES_GRASS = list(Path(PATH_TILES).joinpath("grass").glob("*"))
TILES_WATER = list(Path(PATH_TILES).joinpath("water").glob("*"))

# Tasks

MAZE_START = lambda biome: PurePath(PATH_MAZE_TASK).joinpath(f"{biome}/maze_start.png")
MAZE_END = lambda biome: PurePath(PATH_MAZE_TASK).joinpath(f"{biome}/maze_end.png")
MAZE_PATH = lambda biome: PurePath(PATH_MAZE_TASK).joinpath(f"{biome}/maze_path.png")
MAZE_WALL = lambda biome: PurePath(PATH_MAZE_TASK).joinpath(f"{biome}/maze_wall.png")

# UI assets

# Backgrounds

# Button images
BUTTONS_NAMES = [p.rstrip("png").rstrip(".") for p in listdir(PATH_BUTTONS)]
BUTTONS_PATHS = list(Path(PATH_BUTTONS).glob("*.png"))

BUTTONS = dict(zip(BUTTONS_NAMES, BUTTONS_PATHS))

SLIDER_BODY = PurePath(PATH_SLIDER).joinpath("slider-body.png")
SLIDER_INDICATOR = PurePath(PATH_SLIDER).joinpath("slider-indicator.png")

# Sounds
SOUNDS_BUTTONS_NAMES = [p.rstrip(".ogg").rstrip(".") for p in listdir(PATH_UI_AUDIO)]
SOUND_BUTTONS_PATHS = list(Path(PATH_UI_AUDIO).glob("*.ogg"))

SOUNDS_BUTTONS = dict(zip(SOUNDS_BUTTONS_NAMES, SOUND_BUTTONS_PATHS))

# Music
BG_MUSIC = PurePath(PATH_MUSIC).joinpath("azis.mp3")


class Color:
    """Represent RGB color values."""

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    aqua = (0, 255, 255)
    sky = (207, 239, 252)
    orange = (225, 92, 30)
    green = (0, 255, 0)


class WindowState:
    """Represents windows states."""

    game = "game"
    main_menu = "main_menu"
    options = "options"
    credit = "credit"
    quited = "quit"


class ButtonProperties:
    """Represents buttons properties."""

    main_btn_w = 400
    main_btn_h = 100
    btn_gap = 20

    back_btn_x = 20
    back_btn_y = 20
    back_btn_w = 200
    back_btn_h = 100

    vol_btn_x = 100 + back_btn_x
    vol_btn_y = back_btn_h + 50
    vol_btn_w = 100
    vol_btn_h = 100


class SliderProperties:
    """Represents slider properties."""

    body_x = ButtonProperties.vol_btn_x + 120
    body_y = 200
    body_width = 400
    body_height = 10

    indicator_w = 20
    indicator_h = 60
