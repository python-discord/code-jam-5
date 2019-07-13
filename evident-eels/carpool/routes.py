from flask import render_template, request, flash, abort, redirect, url_for
from carpool import app, db
from carpool.models import User, Carpool
from werkzeug.urls import url_parse
from flask_login import login_required, logout_user, current_user, login_user
from carpool.forms import SignupForm, LoginForm


@app.route("/")
@login_required
def index():
    return render_template("index.html", carpools=Carpool.get_all())


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in to an account
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate():
        print('success')
    if form.validate_on_submit():
        print("Execute validate")
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))
        login_user(user)
        flash("Login successful", "success")
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)
    '''
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("index"))
        else:
            flash("Incorrect username or password", "danger")
            return render_template("login.html")
    '''


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign up for an account
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(name=form.name.data).first():
            flash("Username is already taken", "danger")
            return render_template("signup.html", title="Sign-Up", form=form)
        else:
            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", title="Sign-Up", form=form)
    '''
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_passsword = request.form["confirm_password"]

        error = False
        if not all((username, email, password, confirm_passsword)):
            flash("You must fill in all fields", "danger")
            error = True
        if User.query.filter_by(name=username).first():
            flash("Username is already taken", "danger")
            error = True
        if User.query.filter_by(email=email).first():
            flash("Email is already taken", "danger")
            error = True
        if password != confirm_passsword:
            flash("Passwords do not match", "danger")
            error = True
        if error:
            return render_template("signup.html")

        user = User(name=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash(
            "Signup successful! You may now log in with your new credentials", "success"
        )
        return redirect(url_for("login"))
    '''


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Log out of an account
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/users/<username>")
def users(username):
    """
    View the carpools created by a user
    """

    user = User.query.filter_by(name=username)
    if user:
        # TODO
        # get user's carpools
        pass
    else:
        abort(404)


@app.route("/carpools/<carpool_id>")
def carpools(carpool_id):
    """
    View a particular carpool by its id
    """
    return render_template(
        "carpool.html", carpool=Carpool.query.filter(Carpool.id == carpool_id).first()
    )


@app.route("/search")
def search():
    """
    Search for a user (by username) or carpool (by id)
    """
    if "query" in request.args:
        query = request.args["query"]
    else:
        query = ""

    results = User.query.filter(User.name.like(f"%{query}%")).all()
    if len(results) == 0:
        flash("No results found", "danger")

    return render_template("search.html", query=query, results=results)


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


@app.route("/settings", methods=["GET", "POST"])
def settings():

    pass
