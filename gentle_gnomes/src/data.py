from typing import Tuple

import numpy as np


def get_indicator_data(client, city, indicator) -> Tuple[np.ndarray, np.ndarray]:
    """Return years and averages of indicator data for both historical and RCP85 scenarios."""
    historical = client.get_indicator_data(city, 'historical', indicator)['data']
    rcp85 = client.get_indicator_data(city, 'RCP85', indicator)['data']
    count = len(historical) + len(rcp85)

    x = np.zeros(count, dtype=np.dtype(int))
    y = np.zeros(count, dtype=np.dtype(float))

    for data in (historical, rcp85):
        for i, year in enumerate(data['data']):
            x[i] = int(year)
            y[i] = year['avg']

    return x, y
