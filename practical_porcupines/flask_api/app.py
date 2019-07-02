from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from practical_porcupines.utils import ConfigApi
from practical_porcupines.flask_api.difference_calc import WLDifference


flask_api_app = Flask(__name__)
api = Api(flask_api_app)
wl_dif_obj = WLDifference()

db_url = "sqlite:///waterlevel.sqlite3"

flask_api_app.config["SECRET_KEY"] = ConfigApi().SECRET_KEY
flask_api_app.config["SQLALCHEMY_DATABASE_URI"] = db_url
flask_api_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_api_app)

wl_req = RequestParser(bundle_errors=True)

wl_req.add_argument(
    "date_1",
    type=str,
    required=True
)

wl_req.add_argument(
    "date_2",
    type=str,
    required=True
)

class WaterLevel(Resource):
    def get(self):
        difference, is_prediction = wl_dif_obj.calculate(date_1, date_2)


