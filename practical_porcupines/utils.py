import os
import json
import datetime
from typing import Union


def string_to_datetime(date_string: str) -> Union[datetime.datetime, None]:
    """
    > Func to convert stings in format '%Y:%m:%d:%H:%M:%S' to datetime
      Example:
            string_to_datetime('2010:06:29:17:02:39')
            > datetime.datetime(2010, 6, 29, 17, 2, 39)
            - possible_formats: '2019:06:26:06:26:33', '06:26:33 26.06.2019',
            - '06/26/2019 06:26:33', '26.06.2019', 06/26/2019, 2019-06-29 23:02:05
    - date_string: The string that should be converted
    < Returns Corresponding datetime object
    < Returns If it will be a prediction or not
    x Returns DateFormatError if incoming string isn\'t properly formatted
    """

    possible_formats = [
        "%Y",
        "%Y-%m",
        "%Y/%m",
        "%Y:%m:%d:%H:%M:%S",
        "%H:%M:%S %d.%m.%Y",
        "%m/%d/%Y %H:%M:%S",
        "%d.%m.%Y",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    possible_dates = list()

    for possible_format in possible_formats:
        try:
            possible_dates.append(
                datetime.datetime.strptime(date_string, possible_format)
            )
        except ValueError:
            pass # don't append anything

    if possible_dates:
        date = [date for date in possible_dates][0]
    else:
        date = None

    is_prediction = False

    if date is None:
        raise DateFormatError(
            f"Couldn't match the given date to any template! {date_string}"
        )
    elif not (datetime.date(1993, 1, 15) < date.date() < datetime.date(2019, 2, 7)):
        is_prediction = True

    return date, is_prediction


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


class DateFormatError(BaseException):
    """
    For when the date formatting doesn\'t make sense
    """

    pass


class PredictionNotImplamentedError(BaseException):
    """
    For when predictions are not yet implamented
    and would like to catch
    """

    pass


class ApiReturnBad(BaseException):
    """
    For when API is retuning incorrect values
    """

    pass
