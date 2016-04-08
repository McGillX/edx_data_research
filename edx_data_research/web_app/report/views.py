from flask import render_template
from flask.ext.security import login_required

from . import report
from .forms import BasicReportForm, ProblemIdsReportForm


@report.route('/')
@login_required
def index():
    return render_template('report/index.html')


@report.route('/problemids')
@login_required
def report_problem_ids():
    form = ProblemIdsReportForm()
    return render_template('report/problem_ids.html', form=form)


@report.route('/basic')
@login_required
def report_basic():
    form = BasicReportForm()
    return render_template('report/basic.html', form=form)
