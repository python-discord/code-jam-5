from wtforms import Form, StringField, PasswordField, validators, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class SignupForm(Form):
    """User Signup Form."""

    name = StringField('Name',
                       validators = [DataRequired(message=('Your name here'))])
    email = StringField('Email',
                        validators = [Length(min=6, message=('Please enter a valid email address.')),
                                      Email(message=('Please enter a valid email address.')),
                                      DataRequired(message=('Please enter a valid email address.'))])
    password = PasswordField('Password',
                             validators = [DataRequired(message='Please enter a passwrod.'),
                                           Length(min=6, message=('Please select a stronger password.')),
                                           EqualTo('confirm', message= 'Passwords must match')])
    confirm = PasswordField('Confirm Your Password',)
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class LoginForm(Form):
    """User Login Form."""

    email = StringField('Email', validators = [DataRequired('Please enter a valid emaill address.'),
                                               Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators = [DataRequired('Do not forget your password!?')])
    submit = SubmitField('Log In')
