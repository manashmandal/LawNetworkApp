from . import auth
from .forms import RegistrationForm, LoginForm
from flask import (render_template, redirect, request, url_for, flash)
from app import mongo
from app.models import User, load_user
from flask_login import (login_user, login_required, logout_user, current_user)
from ..viz import viz
from ..main import main

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username' : form.lg_username.data})
        if user is not None and form.lg_password.data == user['password']:
            the_user = load_user(user['username'])
            login_user(the_user)
            flash("Logged in successfully")
            return render_template('about.html')

        flash("Invalid username or password")
    return render_template('login.html', form=form, title="Log In")


# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return render_template('about.html', title="About")


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    form = RegistrationForm()
    if form.validate_on_submit():
        reg_username = form.reg_username.data
        reg_password = form.reg_password.data
        reg_password_confirm = form.reg_password_confirm.data
        reg_email = form.reg_email.data

        # Check if the username exists or not 
        user = mongo.db.users.find_one({'username' : reg_username })

        if user is None and reg_password == reg_password_confirm:
            res = mongo.db.users.insert_one({'username' : reg_username, 'password' : reg_password, 'email' : reg_email })

            if res.acknowledged == True:
                flash("Registered successfully ! Now Login With Your Username and Password")
                return redirect(url_for('auth.login_page'))
        
        flash("Invalid operation ! Username already exists")
    return render_template('register.html', form=form, title="Registration")