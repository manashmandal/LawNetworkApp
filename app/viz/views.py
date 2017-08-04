from flask import render_template
from . import viz
from flask_login import login_required

@viz.route('/viz')
# @login_required
def visualization():
    return render_template('viz.html', title="Visualization")