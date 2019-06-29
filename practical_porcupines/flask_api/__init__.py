from flask_api.app import flask_api_app

# Testing difference calc
from difference_calc import WLDifference
wl_dif = WLDifference()
print(wl_dif.calculate("29:06:2010 17:02:39", "29:06:2019 17:02:39"))
# End testing