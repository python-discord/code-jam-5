from practical_porcupines.flask_api.app import flask_api_app

# Testing difference calc
from practical_porcupines.flask_api.difference_calc import WLDifference
from practical_porcupines.flask_api.models import db, LevelModel

wl_dif = WLDifference()
print(
    "The flask_api testing calculation: "
    + str(wl_dif.calculate("29:06:2010 17:02:39", "29:06:2019 17:02:39"))
)

# db.create_all()
# for i in wl_dif.parse_data():
#     new_row = LevelModel(
#         i[0],
#         i[1]
#     )

#     db.session.add(new_row)
# db.session.commit()
# End testing
