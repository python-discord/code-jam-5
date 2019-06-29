import aiohttp
from practical_porcupines.utils import ConfigApi

config_api = ConfigApi()
aiohttp_session = aiohttp.ClientSession()

API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}/api"


async def get_difference(time_1, time_2):
    """
    > Sends time_1 and time_2 to flask_api
    - time_1 = Start time (%Y:%m:%d:%T)
    - time_2 = End time (%Y:%m:%d:%T)
    < Returns aiohttp response
    x Returns error code 1000 (custom) as in a dict if aiohttp failed
    """

    try:
        return await aiohttp_session.get(API_ENDPOINT, data={"times": [time_1, time_2]})
    except:
        return {"meta": {"status": 1000}}
