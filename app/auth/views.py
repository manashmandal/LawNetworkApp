from . import auth
from .forms import RegistrationForm, LoginForm
from flask import render_template, redirect, request, url_for
from app import mongo
from app.models import User, load_user
from flask_login import login_user, login_required, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    # username = None
    form = LoginForm()
    if form.validate_on_submit():
        print("Validated on submit")
        user = mongo.db.users.find_one({'username' : form.lg_username.data })
        the_user = load_user(user['username'])
        print(user)
        if user is not None and User.validate_login(user['password'], form.lg_password.data):
            print("GOT THE USER")
            login_user(the_user)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    registrationForm = RegistrationForm()
    return render_template('register.html', form=registrationForm)