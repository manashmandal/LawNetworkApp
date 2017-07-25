from wtforms import Form, StringField, validators, PasswordField
from wtforms.validators import DataRequired
from flask import render_template

from . import auth

class LoginForm(Form):
    lg_username = StringField(_name='lg_username', validators=[DataRequired()])
    lg_password = PasswordField(_name='lg_password', validators=[DataRequired()])


class RegistrationForm(Form):
    reg_username = StringField(_name='reg_username', validators=[DataRequired()])
    reg_password = PasswordField(_name='reg_password', validators=[DataRequired()])
    reg_password_confirm = PasswordField(_name='reg_password', validators=[DataRequired()])
    reg_email = StringField(_name='reg_email', validators=[DataRequired()])


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    username = None
    form = LoginForm()
    return render_template('login.html', form=form)




@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    registrationForm = RegistrationForm()
    return render_template('register.html', form=registrationForm)