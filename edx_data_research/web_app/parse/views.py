from flask import render_template
from flask.ext.security import login_required

from . import parse


@parse.route('/')
@login_required
def index():
    return render_template('parse/index.html')


@parse.route('/sql', methods=['GET', 'POST'])
@login_required
def parse_sql():
    return render_template('parse/index.html')

@parse.route('/forum', methods=['GET', 'POST'])
@login_required
def parse_forum():
    return render_template('parse/index.html')


@parse.route('/coursestructure', methods=['GET', 'POST'])
@login_required
def parse_course_structure():
    return render_template('parse/index.html')


@parse.route('/problemids', methods=['GET', 'POST'])
@login_required
def parse_problem_ids():
    return render_template('parse/index.html')


@parse.route('/coursetracking', methods=['GET', 'POST'])
@login_required
def parse_course_tracking():
    return render_template('parse/index.html')