import datetime
import os
import shutil
import tempfile

from flask import render_template, redirect, url_for
from flask.ext.security import login_required, current_user

from . import report
from .forms import BasicReportForm, GeneralStatsForm, ProblemIdsReportForm
from ..args import BasicReport, GeneralStats, ProblemIdsReport
from ..utils import send_email, temp_dir_context
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
        with temp_dir_context() as temp_dir:
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
            subject = 'ProblemIds Report for {0} - {1}'.format(course.capitalize(),
                                                               datetime.datetime.today().date())
            send_email(current_user.email, subject, attachments)
        return redirect(url_for('report.report_problem_ids'))
    return render_template('report/problem_ids.html', form=form)


@report.route('/basic', methods=['GET', 'POST'])
@login_required
def report_basic():
    form = BasicReportForm()
    if form.validate_on_submit():
        with temp_dir_context() as temp_dir:
            course = form.course.data
            report_name = form.report.data
            anonymize = form.anonymize.data
            args = BasicReport(course, 'localhost', report_name, anonymize,
                               temp_dir, 10000)
            edx_obj = reporting.Basic(args)
            getattr(edx_obj, report_name)()

            attachments = [os.path.join(temp_dir, _file)
                           for _file in os.listdir(temp_dir)]
            subject = '{0} Report for {1} - {2}'.format(report_name.capitalize(),
                                                        course.capitalize(),
                                                        datetime.datetime.today().date())
            send_email(current_user.email, subject, attachments)
        return redirect(url_for('report.report_basic'))
    return render_template('report/basic.html', form=form)

@report.route('/stats', methods=['GET', 'POST'])
@login_required
def report_stats():
    form = GeneralStatsForm()
    if form.validate_on_submit():
        with temp_dir_context() as temp_dir:
            course = form.course.data
            anonymize = form.anonymize.data
            args = GeneralStats(course, 'localhost', True, anonymize,
                                temp_dir, 10000)
            edx_obj = reporting.Stats(args)
            edx_obj.stats()

            attachments = [os.path.join(temp_dir, _file)
                           for _file in os.listdir(temp_dir)]
            subject = 'General Stats Report for {0} - {1}'.format(course.capitalize(),
                                                                  datetime.datetime.today().date())
            send_email(current_user.email, subject, attachments)
        return redirect(url_for('report.report_stats'))
    return render_template('report/stats.html', form=form)
