import typing as t

import aiohttp

BASE_URL = 'https://app.climate.azavea.com/api'


class City(t.NamedTuple):
    name: str
    admin: str
    id: int

    def __str__(self):
        return f'{self.name}, {self.admin}'


class Client:
    """Client for interacting with the Azavea Climate API."""

    # Wait for async event loop to instantiate
    session: aiohttp.ClientSession = None

    def __init__(self, token: str):
        self.headers = {'Authorization': f'Token {token}'}

    async def _get(self, endpoint: str, **kwargs) -> t.Union[t.Dict, t.List]:
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers)

        async with self.session.get(BASE_URL + endpoint, **kwargs) as response:
            return await response.json()

    async def teardown(self):
        if self.session is not None:
            await self.session.close()

    async def get_cities(self, **kwargs) -> t.Iterator[City]:
        """Return all available cities."""
        params = {'page': 1}
        params.update(kwargs.get('params', {}))

        while True:
            cities = await self._get('/city', params=params, **kwargs)

            if not cities.get('next'):
                break
            else:
                params['page'] += 1

            for city in cities['features']:
                yield City(city['properties']['name'], city['properties']['admin'], city['id'])

    async def get_nearest_city(
        self,
        lat: str,
        lon: str,
        limit: int = 1,
        **kwargs
    ) -> t.Optional[City]:
        """Return the nearest city to the provided lat/lon or None if not found."""
        params = {
            'lat': lat,
            'lon': lon,
            'limit': limit,
        }

        cities = await self._get('/city/nearest', params=params, **kwargs)

        if cities['count'] > 0:
            city = cities['features'][0]
            return City(city['properties']['name'], city['properties']['admin'], city['id'])

    async def get_scenarios(self, **kwargs) -> t.List:
        """Return all available scenarios."""
        return await self._get('/scenario', **kwargs)

    async def get_indicators(self, **kwargs) -> t.Dict:
        """Return the full list of indicators."""
        return await self._get('/indicator', **kwargs)

    async def get_indicator_details(self, indicator: str, **kwargs) -> t.Dict:
        """Return the description and parameters of a specified indicator."""
        return await self._get(f'/indicator/{indicator}', **kwargs)

    async def get_indicator_data(
        self,
        city: int,
        scenario: str,
        indicator: str,
        **kwargs
    ) -> t.Dict:
        """Return derived climate indicator data for the requested indicator."""
        return await self._get(f'/climate-data/{city}/{scenario}/indicator/{indicator}', **kwargs)
