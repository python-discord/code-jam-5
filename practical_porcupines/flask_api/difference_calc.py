import datetime
import os
import pickle

from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from practical_porcupines.flask_api.models import LevelModel
from practical_porcupines.flask_api.utils import string_to_datetime


class WLDifference:
    def __init__(self):
        # if there is a saved model, load it.
        # re-fitting the model takes time. It is faster to load it from a file
        self.interp_file = Path(
            "practical_porcupines/flask_api/interpolated_function.pkl"
        )
        self.poly_file = Path("practical_porcupines/flask_api/poly_fit_model.pkl")
        if self.interp_file.exists():
            # load it again
            with open(self.interp_file, "rb") as fid:
                self.model = pickle.load(fid)
        else:
            self.model = self._fit_model()

        if os.path.exists(self.poly_file):
            # load it again
            with open(self.poly_file, "rb") as fid:
                self.poly_model = pickle.load(fid)
        else:
            self.poly_model = self._fit_poly_model()

    def calculate(self, date_1, date_2):
        """
        Frontend function for calculating GMWL according to interpolation
        and cubic model predictions. Will get 2 dates and return difference
        and if it was a prediction or not

        > Gets 2 dates
        - date_1: First string date
        - date_2: Second string date
        < Returns float/double: difference in mm
        < Returns bool: if it is a prediction or not
        """

        # make sure both dates are valid and convert them to epoch times
        date_1, is_pred_1 = string_to_datetime(date_1)
        date_2, is_pred_2 = string_to_datetime(date_2)

        # preform calc
        return (
            # fmt: off
            self.evaluate_timestamp(date_2) -
            self.evaluate_timestamp(date_1),
            True if is_pred_1 or is_pred_2 else False  # prediction
        )

    def _fit_model(self):
        """
        Create a mathematical model to estimate any data between 1993 and 2019
        This process takes some time, but will only be called if no model exists

        < Returns `<'scipy.interpolate.interpolate.interp1d'>` class to eval all data in range
        """

        # get all the time and water level values from the database
        dates, water = self._get_all_values()

        # create the model
        model = interp1d(dates, water, kind="cubic")

        # save the interp function
        with open(self.interp_file, "wb") as fid:
            pickle.dump(model, fid)

        return model

    def _fit_poly_model(self):
        """
        Create a mathematical model to estimate any data between before 1993 and after 2019
        This process takes some time, but will only be called if no model exists

        < Returns `<sklearn.linear_model.LinearRegression'>` class to eval all data in range
        """

        def flatten(l):
            return [item for sublist in l for item in sublist]

        X = np.linspace(726188400, 1551999600, 1376352).reshape((-1, 1))
        y = np.array([self.model(x) for x in X])
        X = np.array(flatten(X))
        y = np.array(flatten(y))

        polynomial_features = PolynomialFeatures(degree=3)
        x_poly = polynomial_features.fit_transform(X.reshape(-1, 1))

        poly_model = LinearRegression()
        poly_model.fit(x_poly, y.reshape(-1, 1))

        with open(self.poly_file, "wb") as fid:
            pickle.dump(poly_model, fid)

        return poly_model

    def evaluate_timestamp(self, timestamp):
        if (
            datetime.date(1993, 1, 15) > timestamp.date()
            or datetime.date(2019, 2, 7) < timestamp.date()
        ):
            # perform some data preparation before being able to pass it to the model
            return self.poly_model.predict(
                PolynomialFeatures(degree=3).fit_transform(
                    np.array([timestamp.timestamp()]).reshape(1, -1)
                )
            )

        return self.model(timestamp.timestamp())

    def _get_all_values(self):
        """
        Gets all relevant values from database (LevelModel)

        < Returns waterlevel as a np array
        < Returns date as a np array

        NOTE Both returns corrospond with eachother
        """

        return (
            np.array([lm.wl for lm in LevelModel.query.all()]),  # water level
            np.array([lm.date.timestamp() for lm in LevelModel.query.all()]),  # dates
        )

    def decimal_to_datetime(self, decimal_date):
        """
        Converts the `2017.344858` to a datetime objects

        - decimal_date: the `2017.344858` float
        < Returns datetime object
        """

        year = int(decimal_date)
        rem = decimal_date - year

        base = datetime.datetime(year, 1, 1)

        seconds = (  # fmt: off
            base.replace(year=base.year + 1) - base
        ).total_seconds() * rem

        result = base + datetime.timedelta(seconds=seconds)

        return result

    def parse_data(self):
        """
        Parses the dataset from the NASA file.
        
        < Returns a list of tuples
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
