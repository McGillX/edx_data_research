from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, SelectField
from wtforms.validators import Required


class ParseForm(Form):
    course = SelectField('Course', validators=[Required()],
                         choices=[('atoc185x', 'ATOC185x'),
                         ('atoc185x_2', 'ATOC185x_2'), ('body101x', 'BODY101x'),
                         ('body101x_2', 'BODY101x_2'), ('chem181x', 'CHEM181x'),
                         ('chem181x_2', 'CHEM181x_2'), ('chem181x_3', 'CHEM181x_3'),
                         ('groocx', 'GROOCX'), ('test', 'Test')])
    submit = SubmitField('Submit')


class ForumForm(ParseForm):
    forum_file = FileField('Forum file', validators=[FileRequired()])


class SQLForm(ParseForm):
    collection = SelectField('Collection', validators=[Required()],
                             choices=[('auth_user', 'Auth User'),
                                      ('auth_user_profile', 'Auth User Profile'),
                                      ('student_courseenrollment', 'Student Course Enrollment'),
                                      ('user_id_map', 'User ID Map'),
                                      ('courseware_studentmodule', 'Courseware Student Module'),
                                      ('certificates_generatedcertificate', 'Generated Certificates')])

    sql_file = FileField('SQL file', validators=[FileRequired()])
