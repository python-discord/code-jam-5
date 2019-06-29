from practical_porcupines.utils import ConfigApi
from flask import Flask
# from flask_restful import x # TODO add flask-restful
from flask_sqlalchemy import SQLAlchemy

flask_api_app = Flask(__name__)

flask_api_app.config["SECRET_KEY"] = ConfigApi().SECRET_KEY
flask_api_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waterlevel.sqlite3"
flask_api_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_api_app)
