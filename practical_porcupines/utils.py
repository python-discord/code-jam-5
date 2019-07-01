import os
import json
import datetime


def check_date(date):
    """
    > Gets date
    - String: Date
    < Returns datetime object
    """

    return datetime.datetime.strptime(  # fmt: off
        _add_null_date(date), "%Y:%m:%d:%H:%M:%S"
    )


def _add_null_date(date_match):
    """
    > Gets verified date
    - date_math: verified date from check_date
    < Return stringfied date with extra 00:00:00:00 etc
    """

    output = []
    date_match_split = date_match.split(":")

    date_match_ver = []
    for date_spl in date_match_split:
        if date_spl is not None:
            date_match_ver.append(date_spl)

    for i in range(7):
        if i > len(date_match_ver):
            date_match_ver.append("00")

    return ":".join(date_match_ver)


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


class ApiReturnBad(BaseException):
    """
    When API is retuning incorrect values
    """

    pass
