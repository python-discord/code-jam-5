#
#
#
#
# NOTE this file needs testing
#
#
#
#
#
#

import os
import json


class ConfigBase:
    """
    Basic need-to-know info for all mini-projects
    """

    CONFIG_PATH = "config.json"
    CONFIG = json.load(open(CONFIG_PATH, "r"))
    SHOULD_DEBUG = CONFIG["should_debug"]


class ConfigApi:
    """
    Api endpoints to connect to and host from
    """

    config = ConfigBase().CONFIG

    API_DOMAIN = config["api"]["domain"]
    API_PORT = config["api"]["port"]


class ConfigWebPortal:
    """
    WebPortal endpoints to connect to and host from
    """

    config = ConfigBase().CONFIG

    API_DOMAIN = config["web_portal"]["domain"]
    API_PORT = config["web_portal"]["port"]


class ConfigBot:
    """
    Infomation like the client token for discord_bot mini-project
    """

    def __init__(self):
        self.TOKEN = self._get_bot_token()

    def _get_bot_token(self):
        """
        Returns client token from `CLIENT_TOKEN` env var
        """

        return os.environ["CLIENT_TOKEN"]
