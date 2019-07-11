from datetime import datetime, timedelta
from pathlib import PurePath

from pygame import Rect, Surface
from pygame.image import load

from project.constants import SECONDS_TO_DAYS, WIDTH


def load_img(path: PurePath, convert_alpha: bool = True) -> Surface:
    """Loads an image from path. Optionally enable/disable per-pixel alpha conversion."""
    if convert_alpha:
        return load(str(path)).convert_alpha()
    return load(str(path)).convert()


def fit_to_range(val: float, a: float, b: float, a1: float, b1: float) -> float:
    """Fits a number with range a-b to a new range a1-b1."""
    new_value = ((val - a) / (b - a)) * (b1 - a1) + a1
    return new_value


def realtime_to_ingame_delta(sec: float) -> timedelta:
    """Converts seconds (realtime) to timedelta (ingame)."""
    return timedelta(days=SECONDS_TO_DAYS * sec)


def realtime_to_ingame(sec: float, start_dt: datetime) -> datetime:
    """Converts seconds (realtime) to datetime (ingame), starting from given dt."""
    return start_dt + realtime_to_ingame_delta(sec)


def ingame_delta_formatted(dt: timedelta) -> str:
    """Returns formatted ingame duration survived (text)."""
    return f"{dt.days // 365} years {dt.days % 365} days"


def ingame_formatted(dt: datetime) -> str:
    """Returns formatted ingame timedate(text)."""
    return dt.strftime("%Y - %B")


def realtime_to_ingame_formatted(sec: float, start_dt: datetime) -> str:
    """Converts seconds (realtime) to text, how long the earth lived."""
    return ingame_formatted(realtime_to_ingame(sec, start_dt))


def realtime_to_ingame_delta_formatted(sec: float) -> str:
    """Converts seconds (realtime) to text, how long the earth lived."""
    return ingame_delta_formatted(realtime_to_ingame_delta(sec))


def draw_infinity_bg(screen: Surface, image: Surface, rect1: Rect, rect2: Rect) -> None:
    """
    Draws the infinity backround.

    It uses two rectangles to swap the images.
    The two rectangles are moving in one direction.

    One of them is always with WIDTH ahead of the other rectangle.
    So if it reaches the end, every rectangle goes back with -WIDTH.
    """
    rect1.left += 1
    rect2.left += 1

    if rect1.left == WIDTH:
        rect1.left = -WIDTH
    if rect2.left == WIDTH:
        rect2.left = -WIDTH

    screen.blit(image, rect1)
    screen.blit(image, rect2)
