from flask import Flask

from . import azavea
from . import view


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config.from_pyfile('config.py', silent=True)

    if test_config is not None:
        app.config.from_mapping(test_config)

    app.azavea = azavea.Client(app.config['AZAVEA_TOKEN'])

    app.register_blueprint(view.bp)
    return app
