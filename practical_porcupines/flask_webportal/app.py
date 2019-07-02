from flask import Flask, render_template, request, redirect, url_for,flash
from .forms import DatePickerForm
from flask_bootstrap import Bootstrap
from practical_porcupines.utils import ConfigApi
from ..flask_api.utils import get_datetime
import requests
import os

flask_webportal_app = Flask(__name__)
Bootstrap(flask_webportal_app)
config_api = ConfigApi()
flask_webportal_app.config['SECRET_KEY'] = config_api.SECRET_KEY

@flask_webportal_app.route("/",methods=['GET','POST'])
def index():
    date_picker_form = DatePickerForm()
    if request.method == 'GET':
        return render_template("index.html", form=date_picker_form)
    if date_picker_form.validate_on_submit():
        start_date = request.form.get('start_date') 
        start_date_time = start_date + " 00:00:00"
        end_date = request.form.get('end_date')
        end_date_time = end_date +  + " 00:00:00"
        api_url = f'http://{config_api.API_DOMAIN}:{config_api.API_PORT}'
        request_body = { "times": [
            start_date_time,
            end_date_time
        ] }

        api_response = requests.get(api_url,data=request_body).json()['body']
        wl_difference = api_response['wl_difference']

        wl_string = f'The difference in GMSL between {start_date} and {end_date} was {wl_difference}mm'

        return redirect(url_for('index'), wl_string=wl_string)
    else:
        flash("Invalid Dates!")
        return render_template("index.html", form=date_picker_form)

@flask_webportal_app.route("/about")
def about():
    return render_template("about.html")

@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
