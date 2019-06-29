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

class Config:
    """
    Contains all crutial infomation for this project
    """

    class Base:
        """
        Basic need-to-know info for all mini-projects
        """

        CONFIG_PATH = "config.json"
        CONFIG = json.load(open(CONFIG_PATH, "r"))

    class Api:
        """
        Api endpoints to connect to and host from
        """

        base_config = Config.Base()

        API_DOMAIN = base_config.CONFIG["api"]["domain"]
        API_PORT = base_config.CONFIG["api"]["port"]

    class WebPortal:
        """
        WebPortal endpoints to connect to and host from
        """

        base_config = Config.Base()

        API_DOMAIN = base_config.CONFIG["web_portal"]["domain"]
        API_PORT = base_config.CONFIG["web_portal"]["port"]

    class Bot:
        """
        Infomation like the client token for discord_bot mini-project
        """

        TOKEN = _get_bot_token()

        def _get_bot_token():
            """
            Returns client token from `CLIENT_TOKEN` env var
            """

            return os.environ["CLIENT_TOKEN"]
    