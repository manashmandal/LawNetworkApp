from . import auth
from .forms import RegistrationForm, LoginForm
from flask import render_template



# @auth.route('/register')
# def register_page():
#     return render_template('register.html', title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    # username = None
    form = LoginForm()
    if form.validate_on_submit():
        print("SUBMISSION ASDHASDLHAS JASKD SD")
    else:
        print("not validated")
    return render_template('login.html', form=form)




@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    registrationForm = RegistrationForm()
    return render_template('register.html', form=registrationForm)