import os
import re
import json


def check_date(date):
    """
    > Gets date
    - String: Date
    < Returns matched date
    x Returns None
    """

    date_pattern = (
        "((19[0-9]{2}|2[0-9]{3})((:((0[1-9]|1[012]):"  # year & month
        "([123]0|[012][1-9]|31))(:([01][0-9]|2[0-3]):"  # day and hour
        "([0-5][0-9]):([0-5][0-9]))?)?)?)"  # minute and second
    )

    date_match = re.findall(date_pattern, date)

    if not date_match:
        return None

    return _add_null_date(date_match[0][0])


def _add_null_date(date_match):
    """
    > Gets verified date
    - date_math: verified date from check_date
    < Return stringfied date with extra 00:00:00:00 etc
    """

    output = []
    date_match_split = date_match.split(":")

    # IF date is already full-length
    if len(date_match_split) == 6:
        return date_match

    for i in range(6):
        # NOTE could be done more efficiantly, 6 - len(date_match_split)
        if i > len(date_match_split):
            output.append("00")
        else:
            output.append(date_match[i])

    return ":".join(date_match)


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
