from wtforms import Form, TextField, validators
from wtforms.validators import DataRequired
from flask import render_template

from . import auth

class LoginForm(Form):
    username = TextField('lg_username', validators=[DataRequired()])


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    username = None
    form = LoginForm()
    return render_template('login.html', form=form)


