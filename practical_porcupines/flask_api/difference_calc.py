import os
from typing import Union
from practical_porcupines import utils
from practical_porcupines.flask_api.models import LevelModel
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import numpy as np
from matplotlib import pyplot as plt


class WLDifference:
    def calculate(self, date_1, date_2):
        """
        Calculates difference of global water level between date_1 and date_2
        Returns the difference in mm as a float.
        NOTE This is a frontend function and should hook to lower-level ones
        """
        self._fit_model()
        date_1 = utils.convert_string_to_datetime(utils.check_date(date_1)).timestamp()
        date_2 = utils.convert_string_to_datetime(utils.check_date(date_2)).timestamp()
        if not (date_1 or date_2):
            return None

        return self.evaluate_timestamp(date_1) - self.evaluate_timestamp(date_2)

    def _fit_model(self):
        dates, water = self._get_all_values()

        self.model = interp1d(dates, water, kind='cubic')

    def evaluate_timestamp(self, timestamp):
        return self.model(timestamp)

    @staticmethod
    def _get_all_values():
        water_levels = np.array([lm.wl for lm in LevelModel.query.all()][:964])
        dates = np.array([lm.date.timestamp() for lm in LevelModel.query.all()][:964])
        return dates, water_levels


    def _string_to_datetime(self, decimal_date):
        """
        TODO add Docstring
        """

        year = int(decimal_date)
        rem = decimal_date - year

        base = datetime(year, 1, 1)
        result = base + timedelta(
            seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem
        ).timestamp()

        return result
