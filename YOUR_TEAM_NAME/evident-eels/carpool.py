import os
from flask import Flask, abort, make_response, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    test_carpools = [{
        "user": "fluzz",
        "id": "js832kc",
        "date": "yesterday",
        "location": "my house"
    }]

    return render_template("index.html", carpools=test_carpools)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in to an account
    """

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        pass

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign up for an account
    """

    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        pass

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Log out of an account
    """

    pass

@app.route("/users/<username>")
def users(username):
    """
    View the carpools created by a user
    """

    pass

@app.route("/carpools/<carpool_id>")
def carpools(carpool_id):
    """
    View a particular carpool by its id
    """

    pass

@app.route("/search")
def search():
    """
    Search for a user (by username) or carpool (by id)
    """

    pass

@app.route("/join", methods=["POST"])
def join():
    """
    Join a carpool
    """

    pass

@app.route("/leave", methods=["POST"])
def leave():
    """
    Leave a carpool
    """

    pass

if __name__ == "__main__":
    # server start
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
