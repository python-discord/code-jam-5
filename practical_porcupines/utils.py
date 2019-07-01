import os
import json
from datetime import datetime
from typing import Union


def check_date(date):
    """
    > Gets a short string date
    - date: a string like `2019` or `2005-03-31 00:05:31`
    < Returns [date, time] in int lists
    x Returns DateFormatError if passed date is bad
    x Returns ValueError if date has been formatted wrong
    """

    time_split = date.split(" ")

    if not time_split:
        raise DateFormatError(
            "No dates have been passed into the " "`_add_null_date` function."
        )

    dates = list(map(int, time_split[0].split("-")))
    times = list(map(int, time_split[1].split(":") if len(time_split) > 2 else []))

    for _ in range(3 - len(dates)):
        dates.append(1)

    for _ in range(3 - len(times)):
        times.append(0)

    return [dates, times]


def convert_string_to_datetime(date_string: str) -> Union[datetime, None]:
    """
    > unction to convert stings in the format '%Y:%m:%d:%H:%M:%S' to their datetime representation
      Example:
            convert_string_to_datetime('2010:06:29:17:02:39')
            > datetime.datetime(2010, 6, 29, 17, 2, 39)
    - date_string: The string that should be converted
    < datetime: The corresponding datetime object. If it cant be converted, returns None
    """
    try:
        return datetime.strptime(date_string, '%Y:%m:%d:%H:%M:%S')
    except ValueError:
        return None


class ConfigBase:
    """
    Basic need-to-know info for all mini-projects
    """

    CONFIG_PATH = "config.json"  # Where usually `config.json` is kept
    CONFIG = json.load(open(CONFIG_PATH, "r"))  # Serialized dict from json
    SHOULD_DEBUG = CONFIG["should_debug"]


class ConfigApi:
    """
    Api endpoints to connect to and host from
    """

    config = ConfigBase().CONFIG

    API_DOMAIN = config["api"]["domain"]  # Example: 0.0.0.0
    API_PORT = config["api"]["port"]  # Example: 8080

    def __init__(self):
        self.SECRET_KEY = self._get_secret_key()

    def _get_secret_key(self):
        """
        Returns the secret key for flask_api
        """

        return os.environ["API_SECRET_KEY"]


class ConfigWebPortal:
    """
    WebPortal endpoints to connect to and host from
    """

    config = ConfigBase().CONFIG

    API_DOMAIN = config["web_portal"]["domain"]  # Example: 0.0.0.0
    API_PORT = config["web_portal"]["port"]  # Example: 8080


class ConfigBot:
    """
    Infomation like the client token for discord_bot mini-project
    """

    config = ConfigBase().CONFIG

    PREFIX = config["bot"]["prefix"]  # Gets the prefix to use from CONFIG

    def __init__(self):
        self.TOKEN = self._get_bot_token()  # Discord bot token from env var

    def _get_bot_token(self):
        """
        Returns client token from `CLIENT_TOKEN` env var
        """

        return os.environ["CLIENT_TOKEN"]


class DatesOutOfRange(BaseException):
    """
    For when dates are out of range
    """

    pass


class DateFormatError(BaseException):
    """
    For when the date formatting doesn\'t make sense
    """

    pass


class ApiReturnBad(BaseException):
    """
    When API is retuning incorrect values
    """

    pass
