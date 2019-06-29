import os
import json


class ConfigBase:
    """
    Basic need-to-know info for all mini-projects
    """

    CONFIG_PATH = "config.json"  # Where usually `config.json` is kept
    CONFIG = json.load(open(CONFIG_PATH, "r"))  # Serialized dict from json
    SHOULD_DEBUG = CONFIG["should_debug"]  # The `should_debug` key from the CONFIG dict


class ConfigApi:
    """
    Api endpoints to connect to and host from
    """

    config = ConfigBase().CONFIG

    API_DOMAIN = config["api"]["domain"]  # Example: 0.0.0.0
    API_PORT = config["api"]["port"]  # Example: 8080


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

    def __init__(self):
        self.TOKEN = self._get_bot_token()  # Gets the discord bot token from env var

    def _get_bot_token(self):
        """
        Returns client token from `CLIENT_TOKEN` env var
        """

        return os.environ["CLIENT_TOKEN"]
