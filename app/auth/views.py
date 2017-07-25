from . import auth
from flask import render_template
from config import config
from app import mongo



@auth.route('/register')
def register_page():
    return render_template('register.html', title='Register')