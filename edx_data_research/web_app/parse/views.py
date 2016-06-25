import json
import os
from tempfile import NamedTemporaryFile

from flask import render_template, redirect, url_for
from flask.ext.security import login_required, current_user
from werkzeug import secure_filename

from . import parse
from .forms import (SQLForm, ForumForm, CourseStructureForm, CourseTrackingForm,
                    ProblemIdsForm)
from ..args import SQL, Forum, CourseStructure, CourseTracking, ProblemIdsParse
from ..utils import temp_dir_context
from edx_data_research import parsing

@parse.route('/')
@login_required
def index():
    return render_template('parse/index.html')


@parse.route('/sql', methods=['GET', 'POST'])
@login_required
def parse_sql():
    form = SQLForm()
    if form.validate_on_submit():
        filename = secure_filename(form.sql_file.data.filename)
        with temp_dir_context() as temp_dir:
            file_path = os.path.join(temp_dir, filename)
            sql.forum_file.data.save(file_path)
            course = form.course.data
            collection = forum.collection.data
            args = SQL(course, 'localhost', collection, file_path)
            edx_obj = parsing.SQL(args)
            edx_obj.migrate()
        return redirect(url_for('parse.parse_sql')) 
    return render_template('parse/sql.html', form=form)


@parse.route('/forum', methods=['GET', 'POST'])
@login_required
def parse_forum():
    form = ForumForm()
    if form.validate_on_submit():
        filename = secure_filename(form.forum_file.data.filename)
        with temp_dir_context() as temp_dir:
            file_path = os.path.join(temp_dir, filename)
            form.forum_file.data.save(file_path)
            course = form.course.data
            args = Forum(course, 'localhost', file_path)
            edx_obj = parsing.Forum(args)
            edx_obj.migrate()
        return redirect(url_for('parse.parse_forum')) 
    return render_template('parse/forum.html', form=form)


@parse.route('/coursestructure', methods=['GET', 'POST'])
@login_required
def parse_course_structure():
    form = CourseStructureForm()
    if form.validate_on_submit():
        filename = secure_filename(form.course_structure_file.data.filename)
        with temp_dir_context() as temp_dir:
            file_path = os.path.join(temp_dir, filename)
            form.course_structure_file.data.save(file_path)
            course = form.course.data
            args = CourseStructure(course, 'localhost', file_path, True)
            edx_obj = parsing.CourseStructure(args)
            edx_obj.migrate()
        return redirect(url_for('parse.parse_course_structure'))
    return render_template('parse/course_structure.html', form=form)


@parse.route('/problemids', methods=['GET', 'POST'])
@login_required
def parse_problem_ids():
    form = ProblemIdsForm()
    if form.validate_on_submit():
        course = form.course.data
        args = ProblemIdsParse(course, 'localhost', True)
        edx_obj = parsing.ProblemIds(args)
        edx_obj.migrate()
        return redirect(url_for('parse.parse_problem_ids'))
    return render_template('parse/problem_ids.html', form=form)


@parse.route('/coursetracking', methods=['GET', 'POST'])
@login_required
def parse_course_tracking():
    form = CourseTrackingForm()
    if form.validate_on_submit():
        with NamedTemporaryFile() as temp_file:
            course = form.course.data
            course_ids = form.course_ids.data
            course_ids = [course_id.strip() for course_id in course_ids.split(',')]
            date_of_course_enrollment = form.date_of_course_enrollment.data.strftime('%Y-%m-%d')
            date_of_course_completion = form.date_of_course_completion.data.strftime('%Y-%m-%d')
            json.dump({'course_ids': course_ids,
                       'date_of_course_enrollment': date_of_course_enrollment,
                       'date_of_course_completion': date_of_course_completion},
                      temp_file)
            args = CourseTracking(course, 'localhost', temp_file.name, True)
            edx_obj = parsing.CourseTracking(args)
            edx_obj.migrate()
        return redirect(url_for('parse.parse_course_tracking'))
    return render_template('parse/course_tracking.html', form=form)