from flask import render_template
from . import viz

@viz.route('/viz')
def visualization():
    return render_template('viz_base.html')