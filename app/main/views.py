from flask import render_template
from flask import url_for
from . import main

@main.route('/')
def index():
    return render_template('base.html', title="Hello World")


@main.route('/about')
def about():
    return render_template('about.html', title='About')