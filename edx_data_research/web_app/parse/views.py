from flask import render_template
from flask.ext.security import login_required

from . import parse


@parse.route('/')
@login_required
def index():
    return render_template('parse/index.html')
