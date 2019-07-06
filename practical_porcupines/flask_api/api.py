import datetime
from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from practical_porcupines.flask_api.difference_calc import WLDifference
from practical_porcupines.utils import (
    DateFormatError,
    PredictionNotImplamentedError,
)

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, prefix="/")

wl_dif_obj = WLDifference() # core object init
wl_req = RequestParser(bundle_errors=True) # reqparse init

wl_req.add_argument("date_1", type=str, required=True)
wl_req.add_argument("date_2", type=str, required=True)


class WaterLevel(Resource):
    def get(self):
        args = wl_req.parse_args()

        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        output = {
            "meta": {
                "status_code": 200,
                "dates": {"date_1": args["date_1"], "date_2": args["date_2"]},
                "time_sent": cur_time,
            }
        }

        try:
            wl_difference, is_prediction = wl_dif_obj.calculate(
                # fmt: off
                args["date_1"],
                args["date_2"]
            )
        except DateFormatError:
            status_code = 400
        except PredictionNotImplamentedError:
            status_code = 1002
        else:
            output["body"] = {
                "wl_difference": wl_difference,
                "is_prediction": is_prediction,
            }

            status_code = 200

        output["meta"]["status_code"] = status_code

        return output, 200


api.add_resource(WaterLevel, "/")
