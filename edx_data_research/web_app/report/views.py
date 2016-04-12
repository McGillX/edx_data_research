import datetime
import os
import shutil
import tempfile

from flask import render_template, redirect, url_for
from flask.ext.security import login_required, current_user

from . import report
from .forms import BasicReportForm, ProblemIdsReportForm
from ..args import ProblemIdsReport, SendEmail
from edx_data_research import reporting, tasks


@report.route('/')
@login_required
def index():
    return render_template('report/index.html')


@report.route('/problemids', methods=['GET', 'POST'])
@login_required
def report_problem_ids():
    form = ProblemIdsReportForm()
    if form.validate_on_submit():
        try:
            temp_dir = tempfile.mkdtemp()
            course = form.course.data
            anonymize = form.anonymize.data
            problem_ids = form.problem_ids.data
            problem_ids = [problem_id.strip() for problem_id in problem_ids.split(',')]
            final_attempt = form.final_attempt.data
            include_email = form.include_email.data
            #end_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
            end_date = datetime.datetime(2016, 03, 06).date() - datetime.timedelta(days=1)
            start_date = end_date - datetime.timedelta(days=6)
            args = ProblemIdsReport(course, 'localhost', problem_ids, final_attempt,
                                    include_email, start_date, end_date, temp_dir, 10000,
                                    anonymize, None)
            edx_obj = reporting.ProblemIds(args)
            edx_obj.problem_ids()
            
            attachments = [os.path.join(temp_dir, _file)
                           for _file in os.listdir(temp_dir)]
            from_address = os.environ['FROM_EMAIL_ADDRESS']
            password = os.environ['FROM_EMAIL_PASSWORD']
            to_address = [current_user.email]
            subject = 'Weekly Report for {0} - {1}'.format(course.capitalize(),
                                                           datetime.datetime.today()
                                                           .date())
            args = SendEmail(from_address, None, password, to_address, None,
                             subject, attachments)
            email = tasks.Email(args)
            email.do()
        finally:
            shutil.rmtree(temp_dir)
        return redirect(url_for('report.report_problem_ids'))
    return render_template('report/problem_ids.html', form=form)


@report.route('/basic')
@login_required
def report_basic():
    form = BasicReportForm()
    return render_template('report/basic.html', form=form)
