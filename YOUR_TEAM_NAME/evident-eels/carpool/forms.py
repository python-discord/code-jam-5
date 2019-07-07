from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from carpool.models import User


class SignupForm(FlaskForm):
    """User Signup Form."""

    name = StringField("Name", validators=[DataRequired(message=("Your name here"))])
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
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Your Password")
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
    email = StringField(
        "Email",
        validators=[
            DataRequired("Please enter a valid emaill address."),
            Email("Please enter a valid email address."),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired("Do not forget your password!?")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
