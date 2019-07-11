import aiohttp
from practical_porcupines.utils import (  # fmt: off
    ConfigApi,
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

        await raise_error_codes(resp_jsonized["meta"]["status_code"])


async def raise_error_codes(status_code):
    """
    Raises exceptions depending on the status code

    - status_code: int http status/response code
        x PredictionNotImplamentedError if 1002
        x DateFormatError if 400
    < Returns nothing if passed
    """

    if status_code == 400:
        raise DateFormatError()
    elif status_code == 1002:
        raise PredictionNotImplamentedError()
