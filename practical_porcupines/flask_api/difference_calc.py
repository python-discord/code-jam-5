import os
import pickle
from practical_porcupines.utils import string_to_datetime


class WLDifference:
    def __init__(self):
        # if there is a saved model, load it.
        # re-fitting the model takes time so it is faster to load it from a file
        if os.path.exists("practical_porcupines/flask_api/interpolated_function.pkl"):
            # load it again
            with open(
                "practical_porcupines/flask_api/interpolated_function.pkl", "rb"
            ) as fid:
                self.model = pickle.load(fid)
        else:
            self.model = self._fit_model()

    def calculate(self, date_1, date_2):
        """
        > Gets 2 dates
        - date_1: First string date
        - date_2: Second string date
        < Returns difference in mm
        < Returns if it is a prediction or not (currently always False)
        """
        # make sure both dates are valid and convert them to epoch times
        date_1, is_pred_1 = string_to_datetime(date_1)
        date_2, is_pred_2 = string_to_datetime(date_2)

        if not (date_1 or date_2):
            return None

        # preform calc
        return (
            # fmt: off
            self.evaluate_timestamp(date_1.timestamp()) - 
            self.evaluate_timestamp(date_2.timestamp()),
            True if is_pred_1 or is_pred_2 else False  # prediction
        )

    def _fit_model(self):
        """
        Create a mathematical model to estimate any data between 1993 and 2019
        This process takes some time, but will only be called if no model exists
        < returns '<class 'scipy.interpolate.interpolate.interp1d'>' to eval any data in range
        """

        # get all the time and water level values from the database
        dates, water = self._get_all_values()
        # create the model
        model = interp1d(dates, water, kind="cubic")
        # save the interp function
        with open(
            "practical_porcupines/flask_api/interpolated_function.pkl", "wb"
        ) as fid:
            pickle.dump(model, fid)

        return model

    def evaluate_timestamp(self, timestamp):
        return self.model(timestamp)

    @staticmethod
    def _get_all_values():
        water_levels = np.array([lm.wl for lm in LevelModel.query.all()])
        dates = np.array([lm.date.timestamp() for lm in LevelModel.query.all()])
        return dates, water_levels

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
