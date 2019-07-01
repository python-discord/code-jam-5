from flask import Flask, render_template, request, redirect, url_for
from .forms import DatePickerForm
from flask_bootstrap import Bootstrap
from practical_porcupines.utils import ConfigApi
import os

flask_webportal_app = Flask(__name__)
Bootstrap(flask_webportal_app)
config_api = ConfigApi()
flask_webportal_app.config['SECRET_KEY'] = config_api.SECRET_KEY

@flask_webportal_app.route("/")
def index():
    date_picker_form = DatePickerForm()
    return render_template("index.html", form=date_picker_form)

@flask_webportal_app.route("/", methods=['POST'])
def form_post():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    api_url = f'http://{config_api.API_DOMAIN}:{config_api.API_PORT}'
    return redirect(url_for('index'))

@flask_webportal_app.route("/about")
def about():
    return render_template("about.html")

@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
