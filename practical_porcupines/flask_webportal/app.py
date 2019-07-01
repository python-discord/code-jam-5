from flask import Flask, render_template
from .forms import DatePickerForm
from flask_bootstrap import Bootstrap
import os

flask_webportal_app = Flask(__name__)
Bootstrap(flask_webportal_app)
flask_webportal_app.config['SECRET_KEY'] = os.environ.get('API_SECRET_KEY')

@flask_webportal_app.route("/")
def index():
    date_picker_form = DatePickerForm()
    return render_template("index.html", form=date_picker_form)


@flask_webportal_app.route("/about")
def about():
    return render_template("about.html")

@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
