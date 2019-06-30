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

    @staticmethod
    def decimal_to_datetime(decimal_date):
        year = int(decimal_date)
        rem = decimal_date - year

        base = datetime(year, 1, 1)
        result = base + timedelta(
            seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem
        )

        return result

    @staticmethod
    def parse_data():
        """
        Parses the dataset from the NASA file. returns what we need as a list of tuples
        """
        dataset_path = os.path.join(
            os.path.dirname(__file__), "DATASET_GMSL.txt"
        )
        with open(dataset_path, "r+") as f:
            lines = f.readlines()
            data = list(filter(lambda x: x.find("HDR") == -1, lines))
            filtered_data = []
            for d in data:
                d = d.split()
                reading_date_fraction = float(d[2])
                reading_date = WLDifference.decimal_to_datetime(
                    reading_date_fraction
                ).date()  # Date of GMSL reading
                gmsl = float(d[11])  # GMSL value
                filtered_data.append((reading_date, gmsl))

        return filtered_data
