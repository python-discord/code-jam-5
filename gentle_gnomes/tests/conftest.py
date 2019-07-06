import pytest

from src import create_app
from src.azavea import Client


@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def azavea(app):
    return Client(app.config['AZAVEA_TOKEN'])
