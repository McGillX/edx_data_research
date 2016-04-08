from flask_wtf import Form
from wtforms import SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import Required

class ProblemIdsReportForm(Form):
    course = SelectField('Course', validators=[Required()],
                         choices=[('atoc185x', 'ATOC185x'),
                         ('atoc185x_2', 'ATOC185x_2'), ('body101x', 'BODY101x'),
                         ('body101x_2', 'BODY101x_2'), ('chem181x', 'CHEM181x'),
                         ('chem181x_2', 'CHEM181x_2'), ('chem181x_3', 'CHEM181x_3'),
                         ('groocx', 'GROOCX')])
    problem_ids = TextAreaField('Problem Ids', validators=[Required()])
    final_attempt = BooleanField('Final Attempt Only')
    include_email = BooleanField('Include Email')
    submit = SubmitField('Submit')
