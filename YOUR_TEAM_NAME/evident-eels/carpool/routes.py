from flask import render_template, request
from carpool import app


@app.route("/")
def index():
    test_carpools = [
        {"user": "fluzz", "id": "js832kc", "date": "yesterday", "location": "my house"}
    ]

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
