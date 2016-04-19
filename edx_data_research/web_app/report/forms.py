from flask_wtf import Form
from wtforms import SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import Required


class ReportForm(Form):
    course = SelectField('Course', validators=[Required()],
                         choices=[('atoc185x', 'ATOC185x'),
                         ('atoc185x_2', 'ATOC185x_2'), ('body101x', 'BODY101x'),
                         ('body101x_2', 'BODY101x_2'), ('chem181x', 'CHEM181x'),
                         ('chem181x_2', 'CHEM181x_2'), ('chem181x_3', 'CHEM181x_3'),
                         ('groocx', 'GROOCX')])
    anonymize = BooleanField('Anonymize')
    submit = SubmitField('Submit')


class ProblemIdsReportForm(ReportForm):
    problem_ids = TextAreaField('Problem Ids', validators=[Required()])
    final_attempt = BooleanField('Final Attempt Only')
    include_email = BooleanField('Include Email')


class BasicReportForm(ReportForm):
    report = SelectField('Report', validators=[Required()],
                         choices=[('course_completers', 'Course Completers'),
                                  ('date_of_registration', 'Date of Registration'),
                                  ('forum', 'Forum'), ('ip_to_country', 'IP to Country'),
                                  ('sequential_aggregation', 'Sequential Aggregation'),
                                  ('user_info', 'User Info')])


class GeneralStatsForm(ReportForm):
    pass
