from flask import Flask, render_template

flask_webportal_app = Flask(__name__)


@flask_webportal_app.route("/")
def index():
    return render_template("index.html")


@flask_webportal_app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")
