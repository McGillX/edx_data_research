from flask import render_template
from flask.ext.security import current_user, login_required

from . import users


@users.route('/users/<username>')
@login_required
def users(username):
    pass