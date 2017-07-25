from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired
from flask import render_template

from . import auth

class LoginForm(Form):
    username = StringField('lg_username', validators=[DataRequired()])



@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    username = None
    form = LoginForm()
    return render_template('login.html', form=form)




