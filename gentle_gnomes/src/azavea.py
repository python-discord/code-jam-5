from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Union

import requests

BASE_URL = 'https://app.climate.azavea.com/api'


class City(NamedTuple):
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

    def _get(self, endpoint: str, **kwargs) -> Union[Dict, List]:
        response = self.session.get(BASE_URL + endpoint, ** kwargs)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def _set_param(name: str, value: Any, params: Optional[Dict]) -> Dict:
        """Set a parameter if it isn't already set."""
        value_dict = {name: value}

        if not params:
            params = value_dict
        elif name not in params:
            params.update(value_dict)

        return params

    def get_cities(self, **kwargs) -> Iterator[City]:
        """Return all available cities."""
        params = kwargs.get('params')
        params = self._set_param('page', 1, params)

        while True:
            cities = self._get('/city', params=params, **kwargs)

            if not cities.get('next'):
                break
            else:
                params['page'] += 1

            for city in cities['features']:
                yield City(city['properties']['name'], city['properties']['admin'], city['id'])

    def get_nearest_city(self, lat: float, lon: float, limit: int = 1, **kwargs) -> Optional[City]:
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

    def get_scenarios(self, **kwargs) -> List:
        """Return all available scenarios."""
        return self._get('/scenario', **kwargs)

    def get_indicators(self, **kwargs) -> Dict:
        """Return the full list of indicators."""
        return self._get('/indicator', **kwargs)

    def get_indicator_details(self, indicator: str, **kwargs) -> Dict:
        """Return the description and parameters of a specified indicator."""
        return self._get(f'/indicator/{indicator}', **kwargs)

    def get_indicator_data(self, city: int, scenario: str, indicator: str, **kwargs) -> Dict:
        """Return derived climate indicator data for the requested indicator."""
        return self._get(f'/climate-data/{city}/{scenario}/indicator/{indicator}', **kwargs)
