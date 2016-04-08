from flask import render_template

from . import parse

@parse.route('/')
def index():
    pass
