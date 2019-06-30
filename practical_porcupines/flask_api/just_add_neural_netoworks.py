import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import explained_variance_score, \
    mean_absolute_error, \
    median_absolute_error
import numpy as np
from matplotlib import pyplot
from sklearn.model_selection import train_test_split

# from practical_porcupines.flask_api.models import LevelModel
from practical_porcupines.flask_api.difference_calc import WLDifference

wl_dif = WLDifference()
wl_dif._fit_model()
X = np.linspace(726188400, 1551999600, 10000000).reshape((-1, 1))
y = [wl_dif.evaluate_timestamp(x) for x in X]

X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.2, random_state=23)
X_test, X_val, y_test, y_val = train_test_split(X_tmp, y_tmp, test_size=0.5, random_state=23)

print("Training instances   {}, Training features   {}".format(X_train.shape[0], X_train.shape[1]))
print("Validation instances {}, Validation features {}".format(X_val.shape[0], X_val.shape[1]))
print("Testing instances    {}, Testing features    {}".format(X_test.shape[0], X_test.shape[1]))
