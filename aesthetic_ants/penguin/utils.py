# Contains utility functions
import math


def angle_between(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the angle between the coordinates (x1, y1) and (x2, y2) in radians
    """
    dx = x2 - x1
    dy = y2 - y1

    # We return negative because pyglet and math treat rotation differently
    return -math.atan2(dy, dx)
