from collections import Counter
from typing import Dict, Tuple

import numpy as np
from scipy import stats

INDICATORS = (
    'heat_wave_incidents',
    'total_precipitation',
)


def get_indicator_data(client, city, indicator) -> Tuple[np.ndarray, np.ndarray]:
    """Return years and averages of indicator data for both historical and RCP85 scenarios."""
    historical = client.get_indicator_data(city, 'historical', indicator)['data']
    rcp85 = client.get_indicator_data(city, 'RCP85', indicator)['data']
    count = len(historical) + len(rcp85)

    x = np.zeros(count, dtype=np.dtype(int))
    y = np.zeros(count, dtype=np.dtype(float))

    for scenario in (historical, rcp85):
        for i, data in enumerate(scenario.items()):
            year, values = data
            x[i] = int(year)
            y[i] = values['avg']

    return x, y


def calc_slope(x: np.ndarray, y: np.ndarray) -> float:
    slope, *_ = stats.linregress(x, y)
    return slope


def get_top_indicators(client, city, n: int = 5) -> Dict[str, float]:
    """Return the top n indicators with the highest rate of change."""
    slopes = Counter()
    for indicator in INDICATORS:
        x, y = get_indicator_data(client, city, indicator)
        slopes[indicator] = calc_slope(x, y)

    return dict(slopes.most_common(n))
