import aiohttp
from practical_porcupines.utils import (  # fmt: off
    ConfigApi,
    DatesOutOfRange,
    ApiReturnBad,
)


config_api = ConfigApi()
aiohttp_session = aiohttp.ClientSession()

# API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}/api"
API_ENDPOINT = "https://jilk.pw/api/v1.0/publicall"


async def get_difference(date_1, date_2):
    """
    > Sends date_1 and date_2 to flask_api
    - date_1 = Start time (%Y-%m-%d %T)
    - date_2 = End time (%Y-%m-%d %T)
    < Returns aiohttp response
    """

    payload = {"dates": {"date_1": date_1, "date_2": date_2}}

    async with aiohttp_session.get(API_ENDPOINT, data=payload) as resp:
        resp_jsonized = await resp.json()

        if "body" in resp_jsonized:
            if "wl_difference" in resp_jsonized["body"]:
                # All clear
                return resp_jsonized["body"]["wl_difference"]
            elif resp_jsonized["meta"]["status"] == 1002:
                # Dates out of range
                raise DatesOutOfRange()

        # API returning bad values
        raise ApiReturnBad()
