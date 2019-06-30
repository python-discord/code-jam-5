# Contains utility functions
import math


def angle_between(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the angle between the coordinates (x1, y1) and (x2, y2) in radians
    """
    dx = x1 - x2
    dy = y1 - y2
    return math.atan2(dy, dx)
