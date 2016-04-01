from flask import render_template
from flask.ext.security import current_user, login_required

from . import users


@users.route('/home')
@login_required
def home():
    pass