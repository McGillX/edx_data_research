from flask import render_template

from . import public


@public.route('/')
def index():
    return render_template('public/index.html')


@public.route('/about/')
def about():
    return render_template('public/about.html')