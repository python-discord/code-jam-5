import asyncio
import typing as t
from collections import Counter
from itertools import chain

import numpy as np
from quart import current_app as app
from scipy import stats

from .azavea import City


INDICATORS = (
    'heat_wave_incidents',
    'total_precipitation',
)


class Indicator:
    def __init__(self, name: str, city: int):
        self.name = name
        self.city = city

        self.label = None
        self.description = None
        self.units = None
        self.rate = None
        self.x = None
        self.y = None

    async def _get_data(self) -> t.List[t.Dict]:
        tasks = []
        for scenario in ('historical', 'RCP85'):
            tasks.append(app.azavea.get_indicator_data(self.city, scenario, self.name))

        return await asyncio.gather(*tasks)

    async def populate_data(self):
        """Populate the indicator with data from the API for the historical and RCP85 scenarios."""
        items = []
        count = 0

        for response in await self._get_data():
            self.label = response['indicator']['label']
            self.description = response['indicator']['description']
            self.units = response['units']

            items.append(response['data'].items())
            count += len(response['data'])

        x = np.empty(count, dtype=np.dtype(int))
        y = np.empty(count, dtype=np.dtype(float))

        for i, data in enumerate(chain.from_iterable(items)):
            year, values = data
            x[i] = int(year)
            y[i] = values['avg']

        self.rate = stats.linregress(x, y)[0]

        self.x = x.tolist()
        self.y = y.tolist()

    def to_dict(self) -> t.Dict:
        """Return a dictionary representation of the indicator."""
        return {
            'name': self.name,
            'label': self.label,
            'description': self.description,
            'units': self.units,
            'rate': self.rate,
            'x': self.x,
            'y': self.y
        }


async def _create_indicator(name, city):
    indicator = Indicator(name, city)
    await indicator.populate_data()
    return name, indicator


async def get_top_indicators(city: City, n: int = 5) -> t.Tuple[Indicator, ...]:
    """Return the top n indicators with the highest rate of change."""
    tasks = [_create_indicator(name, city) for name in INDICATORS]
    indicators = dict(await asyncio.gather(*tasks))

    rates = Counter({name: abs(indicator.rate) for name, indicator in indicators.items()})

    return tuple(indicators[k] for k, _ in rates.most_common(n))
