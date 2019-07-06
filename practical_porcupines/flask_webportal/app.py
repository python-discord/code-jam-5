from flask import Flask, render_template, request, redirect, url_for, flash
from .forms import DatePickerForm
from practical_porcupines.utils import ConfigApi
import requests

flask_webportal_app = Flask(__name__)
config_api = ConfigApi()
flask_webportal_app.config["SECRET_KEY"] = config_api.SECRET_KEY


@flask_webportal_app.route("/", methods=["GET", "POST"])
def index():
    date_picker_form = DatePickerForm()
    if request.method == "GET":
        return render_template("index.html", form=date_picker_form)

    if date_picker_form.validate_on_submit():
        start_date = request.form.get("start_date")
        start_date_time = start_date + " 00:00:00"

        end_date = request.form.get("end_date")
        end_date_time = end_date + " 00:00:00"

        api_url = f"http://{config_api.API_DOMAIN}:{config_api.API_PORT}"

        request_body = {"date_1": start_date_time, "date_2": end_date_time}

        try:
            api_response = requests.get(api_url, data=request_body).json()
        except Exception as e:
            Flash(
                "An unknown error occurred when fetching data from the api and "
                f"serializing it! Full error: '{e}'."
            )

            return render_template("index.html", form=date_picker_form)

        if "body" in api_response:
            wl_difference = api_response["body"]["wl_difference"]
            wl_string = f"The difference in GMSL between {start_date} and {end_date} was {wl_difference}mm"
        else:
            status_code = api_response["meta"]["status_code"]

            if status_code == 400:
                flash(
                    "The API has been given a bad date format. This should not "
                    "happen as all of this is automated!"
                )
            elif status_code == 1002:
                flash(
                    "You have gave a date ahead/behind the dataset and "
                    "predictions are not currently implamented!"
                )
            else:
                flash(f"MISC ERROR! Status code: {status_code}")

            return render_template("index.html", form=date_picker_form)

        return render_template("index.html", wl_string=wl_string, form=date_picker_form)

    flash(
        "The dates inputted into the form are not correct, please fix "
        "them according to the format `%Y-%m-%d %T`. An example of this "
        "format is `2019-07-07 12:00:00!"
    )

    return render_template("index.html", form=date_picker_form)


@flask_webportal_app.route("/about")
def about():
    return render_template("about.html")


@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
