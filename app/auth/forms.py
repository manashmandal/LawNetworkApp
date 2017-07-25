from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template

from . import auth

class LoginForm(FlaskForm):
    lg_username = StringField(_name='lg_username', validators=[DataRequired()])
    lg_password = PasswordField(_name='lg_password', validators=[DataRequired()])
    # submit = SubmitField("")


class RegistrationForm(FlaskForm):
    reg_username = StringField(_name='reg_username', validators=[DataRequired()])
    reg_password = PasswordField(_name='reg_password', validators=[DataRequired()])
    reg_password_confirm = PasswordField(_name='reg_password', validators=[DataRequired()])
    reg_email = StringField(_name='reg_email', validators=[DataRequired()])


