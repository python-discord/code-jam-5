import asyncio
import logging
import os
import sys

from quart import Quart

from . import azavea
from . import view

try:
    import uvloop
    uvloop.install()
except ImportError:
    # For some reason asyncio.get_event_loop() fails without this
    asyncio.set_event_loop(asyncio.new_event_loop())


DEBUG = os.getenv('QUART_DEBUG', False)

log = logging.getLogger('src')
log.setLevel(logging.DEBUG if DEBUG else logging.INFO)
log.propagate = True

fmt = '%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s'
formatter = logging.Formatter(fmt)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

log.addHandler(handler)


def create_app(test_config=None):
    app = Quart(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config.from_pyfile('config.py', silent=True)

    if test_config is not None:
        app.config.from_mapping(test_config)

    app.register_blueprint(view.bp)

    app.azavea = azavea.Client(app.config['AZAVEA_TOKEN'])

    @app.after_serving
    async def teardown(*args):
        await app.azavea.teardown()

    return app
