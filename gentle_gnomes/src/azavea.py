from functools import partial
from datetime import datetime

import requests
import aiohttp
import typing as t
import asyncio as aio

BASE_URL = 'https://app.climate.azavea.com/api'


class City(t.NamedTuple):
    name: str
    admin: str
    id: int

    def __str__(self):
        return f'{self.name}, {self.admin}'


class Client:
    """Client for interacting with the Azavea Climate API."""

    def __init__(self, token: str):
        self.headers = {'Authorization': f'Token {token}'}
        self.proxy = AsyncProxy()

    def _get(self, endpoint: str, **kwargs) -> t.Union[t.Dict, t.List]:
        # Update headers with default
        kwargs['headers'] = {**self.headers, **kwargs.get('headers', {})}

        return self.proxy.get(BASE_URL + endpoint, **kwargs)


    def get_cities(self, **kwargs) -> t.Iterator[City]:
        """Return all available cities."""
        params = {'page': 1}
        params.update(kwargs.get('params', {}))

        while True:
            cities = self._get('/city', params=params, **kwargs)

            if not cities.get('next'):
                break
            else:
                params['page'] += 1

            for city in cities['features']:
                yield City(city['properties']['name'], city['properties']['admin'], city['id'])

    def get_nearest_city(self, lat: float, lon: float, limit: int = 1, **kwargs) -> t.Optional[City]:
        """Return the nearest city to the provided lat/lon or None if not found."""
        params = {
            'lat': lat,
            'lon': lon,
            'limit': limit,
        }

        cities = self._get('/city/nearest', params=params, **kwargs)

        if cities['count'] > 0:
            city = cities['features'][0]
            return City(city['properties']['name'], city['properties']['admin'], city['id'])

    def get_scenarios(self, **kwargs) -> t.List:
        """Return all available scenarios."""
        return self._get('/scenario', **kwargs)

    def get_indicators(self, **kwargs) -> t.Dict:
        """Return the full list of indicators."""
        return self._get('/indicator', **kwargs)

    def get_indicator_details(self, indicator: str, **kwargs) -> t.Dict:
        """Return the description and parameters of a specified indicator."""
        return self._get(f'/indicator/{indicator}', **kwargs)

    def get_indicator_data(self, city: int, scenario: str, indicator: str, **kwargs) -> t.Dict:
        """Return derived climate indicator data for the requested indicator."""
        return self._get(f'/climate-data/{city}/{scenario}/indicator/{indicator}', **kwargs)


class AsyncProxy:

    def __init__(self):
        self._pending = []  # [(url, kwargs), ...]

    async def _process_requests(self, *requests: t.Tuple[str, dict]) -> t.Tuple[t.Union[dict, list]]:
        session = aiohttp.ClientSession()

        async def make_request(request):
            url, kwargs = request
            async with session.get(url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

        async with session:
            return await aio.gather(*map(make_request, requests))

    def get(self, url: str, now=True, **kwargs) -> t.Optional[t.Union[dict, list]]:
        """
        Make a get request for the `url` using `kwargs`.

        If `now` is False, store the request for a later. This is to be used with `.collect`, which
        executes the requests concurrently. The response data is returned in the order it was
        recieved.

            ...
            proxy.get(url0, now=False)
            proxy.get(url1, now=False)

            url0_data, url1_data = proxy.collect()
        """
        if now:
            return aio.run(
                self._process_requests((url, kwargs))
            )
        else:
            self._pending.append((url, kwargs))

    def collect(self) -> t.Tuple[t.Union[dict, list]]:
        """Return pending requests in the order they were recieved."""
        result = aio.run(
            self._process_requests(*self._pending)
        )
        self._pending.clear()
        return result
