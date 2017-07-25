from . import auth
from flask import render_template


@auth.route('/login')
def login_page():
    return render_template('login.html', title='Login')


@auth.route('/register')
def register_page():
    return render_template('register.html', title='Register')