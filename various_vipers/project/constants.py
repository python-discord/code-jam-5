"""All game contstants."""
import logging

FPS = 60

WIDTH = 1280
HEIGHT = 720

LOG_LEVEL = logging.DEBUG


class Color:
    """Represent RGB color values."""

    black = (0, 0, 0)
    white = (255, 255, 255)

    red = (255, 0, 0)


class Button:
    """Represents buttons properties."""

    main_btn_w = 400
    main_btn_h = 100
    btn_gap = 50
