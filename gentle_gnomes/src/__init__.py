from flask import Flask

from . import azavea
from . import view


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.azavea = azavea.Client(app.config['AZAVEA_TOKEN'])

    app.register_blueprint(view.bp)
    return app
