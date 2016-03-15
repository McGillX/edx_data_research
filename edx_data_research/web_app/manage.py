#!/usr/bin/python
from flask.ext.script import Manager, Server, Shell

from edx_data_research.web_app import app
from edx_data_research.web_app.models import User, Role

manager = Manager(app)

manager.add_command('run-server', Server(use_debugger=True, use_reloader=True,
                                         host='0.0.0.0'))
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
