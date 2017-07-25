from . import auth
from flask import render_template
from config import config


@auth.route('/login')
def login_page():
    conf = config['development']
    print(conf.DB_NAME)
    return render_template('login.html', title='Login')


@auth.route('/register')
def register_page():
    return render_template('register.html', title='Register')