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
    return render_template('login.html', form=form)

    # # username = None
    # form = LoginForm()
    # if request.method == 'POST':
    #     print("GOT POST")
    #     if form.validate_on_submit():
    #         user = mongo.db.users.find_one({'username' : form.lg_username.data })
            
    #         try:
    #             the_user = load_user(user['username'])
    #             password = user['password']

    #             if (password == form.lg_password.data):
    #                 flash("Password matched!")
    #                 login_user(the_user)
    #                 if (not current_user.is_authenticated):
    #                     return redirect(url_for('auth.login_page'))
    #                 else:
    #                     return redirect(url_for('viz.visualization'))

    #             print(user)
    #         except:
    #             # if user is not None and User.validate_login(user['password'], form.lg_password.data):
    #             #     login_user(the_user)
    #             #     return redirect(request.args.get('next') or url_for('main.index'))
    #             # else:
    #             flash("Username Or Password didn't match")
    #             return redirect(request.args.get('next') or url_for('auth.login_page'))

    # return render_template('login.html', form=form)



# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return render_template('about.html')


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    form = RegistrationForm()
    if form.validate_on_submit():
        reg_username = form.reg_username.data
        reg_password = form.reg_password.data
        reg_password_confirm = form.reg_password_confirm.data
        reg_email = form.reg_email.data
        print("USERNAME : " + reg_username)

        # Check the password if matched
        ## TODO: If not matched show a flash message
        if (reg_password == reg_password_confirm):
            print("PAssword matched")
            return redirect(request.args.get('next') or url_for('main.index'))

        # If password matches then check for username if it exists or not
        if (mongo.db.users.find_one({'username' : reg_username}) != None):
            # TODO: Show flash message that users exists
            print("USER EXISTS")
            return redirect(url_for('auth.register_page'))
        else:
            print("Checking for username")
            print(mongo.db.users.find_one({'username' : reg_username}))


    return render_template('register.html', form=form)