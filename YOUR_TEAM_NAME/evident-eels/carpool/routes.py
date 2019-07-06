from flask import render_template, request
from carpool import app
from carpool.models import User
from flask_login import logout_user
from werkzeug.urls import url_parse
from flask_login import login_required
from carpool.forms import SignupForm


@app.route("/")
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form= form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign up for an account
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign-Up', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Log out of an account
    """
    logout_user()
    return redirect(url_for('index'))



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
