import typing as t

import requests

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
        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Token {token}'}

    def _get(self, endpoint: str, **kwargs) -> t.Union[t.Dict, t.List]:
        response = self.session.get(BASE_URL + endpoint, ** kwargs)
        response.raise_for_status()

        return response.json()

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

    def get_nearest_city(
        self,
        lat: float,
        lon: float,
        limit: int = 1,
        **kwargs
    ) -> t.Optional[City]:
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
