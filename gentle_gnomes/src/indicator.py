import asyncio
import json
from collections import Counter
from itertools import chain
from typing import Tuple

import numpy as np
from quart import current_app as app
from scipy import stats

from .azavea import City


INDICATORS = (
    'heat_wave_incidents',
    'total_precipitation',
)


class Indicator:
    def __init__(self, name: str, city: City):
        self.name = name
        self.city = city

        self.label = None
        self.description = None
        self.units = None
        self.rate = None
        self.plot = None
        self.x = None
        self.y = None

    async def populate_data(self):
        items = []
        count = 0

        for scenario in ('historical', 'RCP85'):
            response = await app.azavea.get_indicator_data(self.city.id, scenario, self.name)
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

        # Convert to JSON just to be safe...
        self.x = json.dumps(x.tolist())
        self.y = json.dumps(y.tolist())


async def _create_indicator(name, city):
    indicator = Indicator(name, city)
    await indicator.populate_data()
    return name, indicator


async def get_top_indicators(city: City, n: int = 5) -> Tuple[Indicator, ...]:
    """Return the top n indicators with the highest rate of change."""
    tasks = [_create_indicator(name, city) for name in INDICATORS]
    indicators = dict(await asyncio.gather(*tasks))

    rates = Counter({name: abs(indicator.rate) for name, indicator in indicators.items()})

    return tuple(indicators[k] for k, _ in rates.most_common(n))
