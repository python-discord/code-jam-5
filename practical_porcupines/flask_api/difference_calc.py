import os
from datetime import datetime, timedelta
from practical_porcupines.flask_api.models import LevelModel


class WLDifference:
    def calculate(self, date_1, date_2):
        """
        Calculates difference of global water level between date_1 and date_2
        Returns the difference in mm as a float.

        NOTE This is a frontend function and should hook to lower-level ones
        """

        pass

    def decimal_to_datetime(self, decimal_date):
        """
        TODO add Docstring
        """

        year = int(decimal_date)
        rem = decimal_date - year

        base = datetime(year, 1, 1)

        seconds = (  # fmt: off
            base.replace(year=base.year + 1) - base
        ).total_seconds() * rem

        result = base + timedelta(seconds=seconds)

        return result

    def parse_data(self):
        """
        > Parses the dataset from the NASA file.
        < List of tuples
        """
        dataset_path = os.path.join(  # fmt: off
            os.path.dirname(__file__), "DATASET_GMSL.txt"
        )

        with open(dataset_path, "r+") as f:
            lines = f.readlines()
            data = list(filter(lambda x: x.find("HDR") == -1, lines))
            filtered_data = []

            for d in data:
                d = d.split()

                reading_date_fraction = float(d[2])

                reading_date = self.decimal_to_datetime(
                    reading_date_fraction
                ).date()  # Date of GMSL reading

                gmsl = float(d[11])  # GMSL value

                filtered_data.append((reading_date, gmsl))

        return filtered_data
