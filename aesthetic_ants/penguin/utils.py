# Contains utility functions
import math
import typing

import pyglet


def angle_between(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the angle between the coordinates (x1, y1) and (x2, y2) in radians
    """
    dx = x2 - x1
    dy = y2 - y1

    # We return negative because pyglet and math treat rotation differently
    return -math.atan2(dy, dx)


def vector_from_angle(angle: float, magnitude: float = 1) -> typing.Tuple[float, float]:
    """
    Returns a vector with a given angle (in radians) and magnitude.
    """
    x = math.cos(angle) * magnitude
    y = math.sin(angle) * magnitude
    return x, y


def distance_between(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the distance between the two points (x1, y1) and (x2, y2)
    """
    return distance_between_sq(x1, y1, x2, y2)**0.5


def distance_between_sq(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the squared distance between the two points (x1, y1) and (x2, y2)
    """
    dx = x2 - x1
    dy = y2 - y1
    return dx**2 + dy**2


def circles_collide(x1: float, y1: float, r1: float, x2: float, y2: float, r2: float) -> bool:
    """
    Returns whether the two circles (x1, y1), r1 and (x2, y2), r2 overlap
    """
    return distance_between_sq(x1, y1, x2, y2) <= (r1 + r2)**2


keys = pyglet.window.key.KeyStateHandler()
