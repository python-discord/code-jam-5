from flask import Flask, render_template

flask_webportal_app = Flask(__name__)

@flask_webportal_app.route("/")
def index():
    return render_template("index.html")
