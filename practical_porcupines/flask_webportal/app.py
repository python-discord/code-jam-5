from flask import Flask, render_template
from .forms import DatePickerForm

flask_webportal_app = Flask(__name__)


@flask_webportal_app.route("/")
def index():
    return render_template("index.html")


@flask_webportal_app.route("/about")
def about():
    return render_template("about.html")


@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
