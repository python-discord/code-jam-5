import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "testing123"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

from carpool import routes, models  # noqa


def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
