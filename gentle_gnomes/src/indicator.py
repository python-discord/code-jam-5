from collections import Counter
from itertools import chain
from typing import Tuple

import numpy as np
from flask import current_app as app
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
        self._populate_data()

    def _populate_data(self):
        items = []
        count = 0

        for scenario in ('historical', 'RCP85'):
            response = app.azavea.get_indicator_data(self.city.id, scenario, self.name)
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

        self.rate = self._calc_slope(x, y)

    @staticmethod
    def _calc_slope(x: np.ndarray, y: np.ndarray) -> float:
        slope, *_ = stats.linregress(x, y)
        return slope


def get_top_indicators(city: City, n: int = 5) -> Tuple[Indicator, ...]:
    """Return the top n indicators with the highest rate of change."""
    rates = Counter()
    indicators = {}

    for name in INDICATORS:
        indicator = Indicator(name, city)

        rates[name] = indicator.rate
        indicators[name] = indicator

    return tuple(indicators[k] for k, _ in rates.most_common(n))
