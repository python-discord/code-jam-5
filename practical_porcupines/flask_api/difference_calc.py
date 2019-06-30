import os
from practical_porcupines.flask_api.models import LevelModel
from datetime import datetime, timedelta


class WLDifference:
    def calculate(date_1, date_2):
        """
        Calculates difference of global water level between date_1 and date_2
        Returns the difference in mm as a float.
        NOTE This is a frontend function and should hook to lower-level ones
        """
        pass

    def _string_to_datetime(self, decimal_date):
        """
        TODO add Docstring
        """

        year = int(decimal_date)
        rem = decimal_date - year

        base = datetime(year, 1, 1)
        result = base + timedelta(
            seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem
        )

        return result
