from flask import Flask

app = Flask(__name__)

from carpool import routes # noqa
