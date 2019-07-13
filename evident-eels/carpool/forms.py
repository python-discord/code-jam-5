from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from carpool.models import User


class SignupForm(FlaskForm):
    """User Signup Form."""

    name = StringField("Name", validators=[DataRequired(message=('Please enter a username'))])
    email = StringField(
        "Email",
        validators=[
            Length(min=6, message=("Please enter a valid email address.")),
            Email(message=("Please enter a valid email address.")),
            DataRequired(message=("Please enter a valid email address.")),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter a passwrod."),
            Length(min=6, message=("Please select a stronger password.")),
        ],
    )
    confirm = PasswordField("Confirm Your Password", validators=[
        EqualTo('password', message="Passwords must match")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    """User Login Form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password", validators=[DataRequired("Do not forget your password!?")])
    submit = SubmitField("Log In")
