import aiohttp
from practical_porcupines.utils import (  # fmt: off
    ConfigApi,
    ApiReturnBad,
    PredictionNotImplamentedError,
    DateFormatError,
)


config_api = ConfigApi()
aiohttp_session = aiohttp.ClientSession()

API_ENDPOINT = f"http://{config_api.API_DOMAIN}:{config_api.API_PORT}"


async def get_difference(date_1, date_2):
    """
    > Sends date_1 and date_2 to flask_api
    - date_1 = Start time (%Y-%m-%d %T)
    - date_2 = End time (%Y-%m-%d %T)
    < Returns difference in mm
    """

    payload = {"date_1": date_1, "date_2": date_2}

    async with aiohttp_session.get(API_ENDPOINT, data=payload) as resp:
        resp_jsonized = await resp.json()

        if "body" in resp_jsonized:
            if "wl_difference" in resp_jsonized["body"]:
                return (
                    resp_jsonized["body"]["wl_difference"],
                    resp_jsonized["body"]["is_prediction"],
                )

            raise_error_codes(status_code)

        raise ApiReturnBad()


async def add_embeds(status_code, discord):
    """
    > Gets status code
    - status_code: int http return code
    < Raises errors
    x Does nothing
    """

    if status_code == 400:
        raise DateFormatError()
    elif status_code == 1002:
        raise PredictionNotImplamentedError()
