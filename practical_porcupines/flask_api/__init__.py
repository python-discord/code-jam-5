from practical_porcupines.flask_api.app import flask_api_app

# Testing difference calc
from practical_porcupines.flask_api.difference_calc import WLDifference

wl_dif = WLDifference()
print(
    "The flask_api testing calculation: "
    + str(wl_dif.calculate("29:06:2010 17:02:39", "29:06:2019 17:02:39"))
)
# End testing
