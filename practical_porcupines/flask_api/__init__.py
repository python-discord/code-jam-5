import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from practical_porcupines.utils import ConfigApi

flask_api_app = Flask(__name__)

db_url = "sqlite:///waterlevel.sqlite3"

flask_api_app.config["SECRET_KEY"] = ConfigApi().SECRET_KEY
flask_api_app.config["SQLALCHEMY_DATABASE_URI"] = db_url
flask_api_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_api_app)

# NOTE Blueprint inits have to be below db init or the views cannot access the DB
from practical_porcupines.flask_api.api import api_blueprint

flask_api_app.register_blueprint(api_blueprint, url_prefix="/")
