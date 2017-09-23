import os
from app import *
from flask_script import Manager, Shell

app = create_app('development')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, mongo=mongo)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
