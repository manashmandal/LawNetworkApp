from . import auth
from flask import render_template
from config import config
from app import mongo


@auth.route('/login')
def login_page():
    print(mongo.db.users.find_one({'id' : 1}))
    return render_template('login.html', title='Login')


@auth.route('/register')
def register_page():
    return render_template('register.html', title='Register')