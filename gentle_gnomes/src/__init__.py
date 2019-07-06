import uvloop
from quart import Quart

from . import azavea
from . import view

uvloop.install()

def create_app(test_config=None):
    app = Quart(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config.from_pyfile('config.py', silent=True)

    if test_config is not None:
        app.config.from_mapping(test_config)

    app.register_blueprint(view.bp)

    app.azavea = azavea.Client(app.config['AZAVEA_TOKEN'])

    @app.teardown_appcontext
    async def teardown(*args):
        await app.azavea.teardown()

    return app
