import os
import sys
from collections import namedtuple

from edx_data_research import parsing

DIRECTORY = '/data/{0}'


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


if __name__ == '__main__':
    main()
