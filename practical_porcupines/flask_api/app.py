from practical_porcupines.utils import ConfigApi
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser

flask_api_app = Flask(__name__)
api = Api(flask_api_app)

db_url = "sqlite:///waterlevel.sqlite3"

flask_api_app.config["SECRET_KEY"] = ConfigApi().SECRET_KEY
flask_api_app.config["SQLALCHEMY_DATABASE_URI"] = db_url
flask_api_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_api_app)

wl_req = RequestParser(bundle_errors=True)

wl_req.add_argument(
    
)
