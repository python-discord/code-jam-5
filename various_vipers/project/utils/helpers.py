import datetime

from project.constants import SECONDS_TO_DAYS


def fit_to_range(val: float, a: float, b: float, a1: float, b1: float) -> float:
    """Fits a number with range a-b to a new range a1-b1."""
    new_value = ((val - a) / (b - a)) * (b1 - a1) + a1
    return new_value


def realtime_to_ingame_delta(sec: float) -> datetime.timedelta:
    """Converts seconds (realtime) to timedelta (ingame)."""
    return datetime.timedelta(days=SECONDS_TO_DAYS * sec)


def realtime_to_ingame(sec: float, start_dt: datetime.datetime) -> datetime.datetime:
    """Converts seconds (realtime) to datetime (ingame), starting from given dt."""
    return start_dt + realtime_to_ingame_delta(sec)


def ingame_delta_formatted(dt: datetime.timedelta) -> str:
    """Returns formatted ingame duration survived (text)."""
    return f"{dt.days // 365} years {dt.days % 365} days"


def ingame_formatted(dt: datetime.datetime) -> str:
    """Returns formatted ingame timedate(text)."""
    return dt.strftime("%Y - %B")


def realtime_to_ingame_formatted(sec: float, start_dt: datetime.datetime) -> str:
    """Converts seconds (realtime) to text, how long the earth lived."""
    return ingame_formatted(realtime_to_ingame(sec, start_dt))


def realtime_to_ingame_delta_formatted(sec: float) -> str:
    """Converts seconds (realtime) to text, how long the earth lived."""
    return ingame_delta_formatted(realtime_to_ingame_delta(sec))
