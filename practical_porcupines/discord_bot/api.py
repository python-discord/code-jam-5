import aiohttp
from practical_porcupines.utils import ConfigApi

config_api = ConfigApi()
aiohttp_session = aiohttp.ClientSession(auth=auth)

API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}/api"

async def get_difference(time_1, time_2):
    """
    > Sends time_1 and time_2 to flask_api
    - time_1 = Start time (%Y:%m:%d:%T)
    - time_2 = End time (%Y:%m:%d:%T)
    < Returns float of mm difference
    x Returns error message as a string if aiohttp failed
    """

    try:
