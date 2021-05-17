from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from .models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=1, max=20)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password1', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def valid_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('This email has been registered, please log in or sign up with a different one.')
        

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def valiate_email(self,email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise ValidationError('There is no account related to that email, please sign up first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password1', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')