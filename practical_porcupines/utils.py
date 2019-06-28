import json

class Config:
    class Base:
        CONFIG_PATH = "config.json"
        CONFIG = json.load(open(CONFIG_PATH, "r"))

    class Api:
        base_config = Base()

        API_DOMAIN = base_config.CONFIG["api"]["domain"]
        API_PORT = base_config.CONFIG["api"]["port"]
