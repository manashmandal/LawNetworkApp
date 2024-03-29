import os
from app import *
from flask_script import Manager, Shell
from flask import Flask


app = create_app('development')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, mongo=mongo)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,  debug=True)
    # manager.run()
