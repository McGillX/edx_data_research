#!/usr/bin/python
from flask.ext.script import Manager, Server, Shell

from edx_data_research.web_app import create_app
from edx_data_research.web_app.models import User, Role


app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('clean', Clean())
manager.add_command('server', Server(use_debugger=True, use_reloader=True,
                                         host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('urls', ShowUrls())


if __name__ == '__main__':
    manager.run()