import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from practical_porcupines.flask_api.difference_calc import WLDifference
from practical_porcupines.flask_api.models import LevelModel


def _get_all_values():
    water_levels = np.array([lm.wl for lm in LevelModel.query.all()][:964])
    dates = np.array([lm.date.timestamp() for lm in LevelModel.query.all()][:964])
    return dates, water_levels


wl_dif = WLDifference()
wl_dif._fit_model()
X = np.linspace(726188400, 1551999600, 10000000).reshape((-1, 1))
y = [wl_dif.evaluate_timestamp(x) for x in X]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

# instantiate the regressor class
regressor = LinearRegression()

# fit the build the model by fitting the regressor to the training data
regressor.fit(X_train, y_train)

prediction = regressor.predict(X_test)

# Evaluate the prediction accuracy of the model
from sklearn.metrics import mean_absolute_error, median_absolute_error
print("The Explained Variance: %.5f" % regressor.score(X_test, y_test))
print("The Mean Absolute Error: %.2f mm" % mean_absolute_error(y_test, prediction))
print("The Median Absolute Error: %.2f mm" % median_absolute_error(y_test, prediction))

import pickle
# save the classifier
with open('learned_classifier.pkl', 'wb') as fid:
    pickle.dump(regressor, fid)

# # load it again
# with open('learned_classifier.pkl', 'rb') as fid:
#     regressor_loaded = pickle.load(fid)

"""
10000000: 
The Explained Variance: 0.97620
The Mean Absolute Error: 3.02 mm
The Median Absolute Error: 2.54 mm

1000000:

The Explained Variance: 0.97624
The Mean Absolute Error: 3.03 mm
The Median Absolute Error: 2.55 mm

100000:

The Explained Variance: 0.97606
The Mean Absolute Error: 3.04 mm
The Median Absolute Error: 2.56 mm

10000:

The Explained Variance: 0.97537
The Mean Absolute Error: 3.02 mm
The Median Absolute Error: 2.51 mm

1000:

The Explained Variance: 0.97583
The Mean Absolute Error: 2.91 mm
The Median Absolute Error: 2.08 mm

100:
The Explained Variance: 0.96613
The Mean Absolute Error: 3.67 mm
The Median Absolute Error: 3.27 mm

10:
The Explained Variance: 0.93015
The Mean Absolute Error: 5.33 mm
The Median Absolute Error: 5.33 mm
"""

