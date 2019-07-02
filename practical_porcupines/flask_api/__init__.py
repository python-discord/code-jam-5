from practical_porcupines.flask_api.app import flask_api_app  # noqa

# Testing difference calc
from practical_porcupines.flask_api.difference_calc import WLDifference

wl_dif = WLDifference()
print(
    "The flask_api testing calculation: "
    + str(wl_dif.calculate("2010:06:29:17:02:39", "2019:01:29:17:02:39"))
)
# End testing
