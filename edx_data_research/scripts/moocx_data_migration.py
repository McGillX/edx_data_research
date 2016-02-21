import datetime
import os
import sys
import tempfile
from collections import namedtuple

from edx_data_research import parsing, reporting, tasks

DIRECTORY = '/data/{0}'
LOG_FILE = '/data/{0}_logs.txt'
TRACKING_LOGS_REPORT = 'tracking_logs_monitoring_report.csv'


def migrate_sql_data(db):
    Args = namedtuple('Args', ['db_name', 'uri', 'collection', 'sql_file'])
    collections = frozenset(['auth_user', 'student_courseenrollment',
                             'user_id_map', 'courseware_studentmodule',
                             'auth_userprofile',
                             'certificates_generatedcertificate'])
    sql_file_format = 'McGillX-Body101x-1T2016-{0}-prod-analytics.sql'
    for collection in collections:
        sql_file_path = os.path.join(DIRECTORY.format(db),
                                     sql_file_format.format(collection))
        args = Args(db, 'localhost', collection, sql_file_path)
        print 'Migrating SQL data to collection {0}'.format(collection)
        edx_obj = parsing.SQL(args)
        edx_obj.migrate()


def migrate_forum_data(db):
    Args = namedtuple('Args', ['db_name', 'uri', 'forum_file'])
    forum_file_path = os.path.join(DIRECTORY.format(db),
                                   'McGillX-Body101x-1T2016-prod.mongo')
    args = Args(db, 'localhost', forum_file_path)
    print 'Migrating forum data to collection forum'
    edx_obj = parsing.Forum(args)
    edx_obj.migrate()


def migrate_course_structure_data(db):
    Args = namedtuple('Args', ['db_name', 'uri', 'course_structure_file', 'drop'])
    course_structure_file_path = os.path.join(DIRECTORY.format(db),
                                     'McGillX-Body101x-1T2016-course_structure-prod-analytics.json')
    args = Args(db, 'localhost', course_structure_file_path, True)
    print 'Migrating course_structure data to collection course_structure'
    edx_obj = parsing.CourseStructure(args)
    edx_obj.migrate()


def migrate_course_tracking(db, course_config_file):
    Args = namedtuple('Args', ['db_name', 'uri', 'course_config_file', 'drop'])
    args = Args(db, 'localhost', course_config_file, True)
    print 'Migrating course specific tracking data to collection tracking'
    edx_obj = parsing.CourseTracking(args)
    edx_obj.migrate()
    

def migrate_problem_ids(db):
    Args = namedtuple('Args', ['db_name', 'uri', 'drop'])
    args = Args(db, 'localhost', True)
    print 'Migrating problem ids data to collection problem_ids'
    edx_obj = parsing.ProblemIds(args)
    edx_obj.migrate()


def generate_problem_ids_reports(db, output_dir=os.getcwd()):
    Args = namedtuple('Args', ['db_name', 'uri', 'problem_ids', 'final_attempt',
                               'include_email', 'start_date', 'end_date', 'output'])
    problem_ids = ['block-v1:McGillX+Body101x+1T2016+type@problem+block@b89c2e954e36457fbe77047db34a601b',
                   'block-v1:McGillX+Body101x+1T2016+type@problem+block@149365c1111646038182c8b1b726d1ac',
                   'block-v1:McGillX+Body101x+1T2016+type@problem+block@07b2371ef7514c6b94a9f545e38a041c',
                   'block-v1:McGillX+Body101x+1T2016+type@problem+block@7e23b88574354d8cabef0606e5c45534'
                  ]
    end_date = datetime.datetime.today().date()
    start_date = end_date - datetime.timedelta(days=7)
    args = Args(db, 'localhost', problem_ids, True, True, start_date, end_date,
                output_dir)
    print 'Generating report for problem ids'
    edx_obj = reporting.ProblemIds(args)
    edx_obj.problem_ids()


def send_email_report(db, attachments_dir=os.getcwd()):
    Args = namedtuple('Args', ['from_address', 'from_name', 'password',
                               'to_address', 'body', 'subject', 'attachments'])
    attachments = [os.path.join(attachments_dir, _file)
                   for _file in os.listdir(attachments_dir)]
    attachments.extend(_attach_additional_files(db))
    from_address = os.environ['FROM_EMAIL_ADDRESS']
    password = os.environ['FROM_EMAIL_PASSWORD']
    to_address = os.environ['TO_EMAIL_ADDRESS']
    subject = 'Weekly Report for {0} - {1}'.format(db.capitalize(),
                                                   datetime.datetime.today()
                                                   .date())
    args = Args(from_address, None, password, to_address, None, subject,
                attachments)
    print 'Sending email of report to {0}'.format(to_address)
    email = tasks.Email(args)
    email.do()


def _attach_additional_files(db):
    files = [LOG_FILE.format(db)]
    home_directory = os.path.expanduser('~')
    tracking_logs_report = os.path.join(home_directory, TRACKING_LOGS_REPORT)
    files.append(tracking_logs_report)
    return files


def main():
    if len(sys.argv) != 3:
        raise ValueError('Must pass course database name and course config file')
    db_name, config_file = sys.argv[1:]
    print 'Starting migration of data for course {0}'.format(db_name)
    migrate_sql_data(db_name)
    migrate_forum_data(db_name)
    migrate_course_structure_data(db_name)
    migrate_course_tracking(db_name, config_file)
    migrate_problem_ids(db_name)
    try:
        temp_dir = tempfile.mkdtemp()
        generate_problem_ids_reports(db_name, temp_dir)
        send_email_report(db_name, temp_dir)
    finally:
        os.removedirs(temp_dir)


if __name__ == '__main__':
    main()