import aiohttp
from practical_porcupines.utils import ConfigApi

config_api = ConfigApi()

API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}"
