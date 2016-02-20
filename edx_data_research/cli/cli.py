import Queue
import argparse
import collections
import os
import sys
from datetime import datetime

from edx_data_research.cli import commands

def valid_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)

def main():
    parser = argparse.ArgumentParser(prog='moocx',
                                     description='EdX MOOC Data Anaylysis')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1.0')

    subparsers = parser.add_subparsers(metavar='<command>', dest='command')

    # A parser for parsing and migrating data to a database
    parse_parser = subparsers.add_parser('parse',
                                         help='Parse edX course data and '
                                         'migrate to MongoDB database')
    parse_parser.add_argument('db_name',
                              help='Name of database where each database '
                              'corresponds to a course offering')
    parse_parser.add_argument('-u', '--uri', help='URI to MongoDB database '
                              '(default: mongodb://localhost:27017)')

    parse_subparsers = parse_parser.add_subparsers(metavar='<parse>', dest='parse')

    parse_sql = parse_subparsers.add_parser('sql', help='Migrate SQL files')
    parse_sql.add_argument('collection', choices=['auth_user',
                           'student_courseenrollment', 'user_id_map',
                           'courseware_studentmodule', 'auth_userprofile',
                           'certificates_generatedcertificate'],
                           help='Name of collection where data is to be '
                           'migrated')
    parse_sql.add_argument('sql_file', help='Path to SQL file to migrate')

    parse_forum = parse_subparsers.add_parser('forum', help='Migrate Forum data')
    parse_forum.add_argument('forum_file', help='Path to Forum data file to migrate')

    parse_problem_ids = parse_subparsers.add_parser('problem-ids',
                                                    help='Generate problem ids '
					            'collection from the tracking logs collection')
    parse_course_structure.add_argument('-d', '--drop', action=store_true,
                                        help='Drop collection')

    parse_course_structure = parse_subparsers.add_parser('course_structure',
                                                         help='Migrate Course Structure data')
    parse_course_structure.add_argument('course_structure_file',
                                        help='Path to Course Structure data file to migrate')
    parse_course_structure.add_argument('-d', '--drop', action=store_true,
                                        help='Drop collection')

    parse_tracking = parse_subparsers.add_parser('tracking',
                                                 help='Migrate tracking logs')
    parse_tracking.add_argument('logs', nargs='+', help='Path to log files; '
                                'these can be files or folders containing log '
                                'files (files could also be zipped files)')
    
    parse_course_tracking = parse_subparsers.add_parser('course-tracking',
                                                        help='Extract course'
                                                        'specific tracking logs'
                                                        'from tracking database'
                                                        'to course database')
    parse_course_tracking.add_argument('course_config_file', help='Config file'
                                       'to load configurations about a course.'
                                       'For example, pass example as argument')
    parse_course_tracking.add_argument('-d', '--drop', action=store_true,
                                       help='Drop collection')

    # An report parser to execute the analysis and/or generate CSV reports
    report_parser = subparsers.add_parser('report',
                                          help='Report commands to execute the '
                                          'analysis and/or generate CSV reports')
    report_parser.add_argument('db_name',
                               help='Name of database where each database '
                               'corresponds to a course offering')
    report_parser.add_argument('-u', '--uri', help='URI to MongoDB database '
                            '(default: mongodb://localhost:27017)')
    report_parser.add_argument('-o', '--output', help='Path to directory to '
                               'save CSV report (defaults to current directory: '
                               '%(default)s)', default=os.getcwd(),
                               dest='output_directory')
    report_parser.add_argument('-r', '--row-limit', help='Number of rows per '
                               'file (default: %(default)s)', type=int,
                                default=100000, dest='row_limit')
    report_parser.add_argument('-a', '--anonymize', help='Only include hash id '
                               'of the students in output CSV report '
                               '(default: %(default)s)', action='store_true')

    report_subparsers = report_parser.add_subparsers(metavar='<report>', dest='report')

    report_basic = report_subparsers.add_parser('basic', help='Run basic '
                                                'report generation commands')
    report_basic.add_argument('basic', help='Run analytics based on argument')

    report_problem_ids = report_subparsers.add_parser('problem-ids',
                                                      help='Generate CSV '
                                                      'reports for given problem ids')
                                                     
    report_problem_ids.add_argument('problem_ids', nargs='+', help='Problem ID')
    report_problem_ids.add_argument('-f', '--final-attempt', action='store_true',
                                    help='Only include students\' final attempt '
                                    'to the given problem ids')
    report_problem_ids.add_argument('-e', '--include-email', action='store_true',
                                    help="Include students' email address in report")
    report_problem_ids.add_argument('-d', '--display-names', nargs='+',
                                    help='Take list of display names in same  '
                                    'order as problem ids')
    group = report_problem_ids.add_argument_group('dates')
    group.add_argument('-s', '--start-date', help='Start date',
                                    type=valid_date)
    group.add_argument('-t', '--end-date', help='End date',
                                    type=valid_date)
                                   
    # A stats command to print basic stats about given course
    report_stats = report_subparsers.add_parser('stats', help='Report commands')
    report_stats.add_argument('-c', '--csv', help='Print output to a csv report '
                               '(default: %(default)s)', action='store_true')
                               
    # An task parser to run operational tasks
    task_parser = subparsers.add_parser('task',
                                          help='Task commands to run '
                                          'operational tasks')
    task_subparsers = task_parser.add_subparsers(metavar='<task>', dest='task')
    
    task_email = task_subparsers.add_parser('email', help='Send email')
    task_email.add_argument('-f', '--from-address', help='Email address to send from')
    task_email.add_argument('-n', '--from-name', help='Name of sender')
    task_email.add_argument('-p', '--password', help='Password')
    task_email.add_argument('-t', '--to-address', nargs='+',
                            help='Email addresses to send to')
    task_email.add_argument('-b', '--body', help='Email body read from a file')
    task_email.add_argument('-s', '--subject', help='Email subject')
    task_email.add_argument('-a', '--attachments', nargs='+',
                            help='Attachments to include in report')
    

    def get_subparsers(parser):
        subparsers = set()
        queue = Queue.Queue()
        queue.put(parser)
        while not queue.empty():
            _subparser = queue.get()
            for action in _subparser._actions:
                if isinstance(action, argparse._SubParsersAction):
                    [queue.put(item) for item in action.choices.values()]
                    subparsers.update(action.choices.keys())
                    break
        return subparsers

    subparsers = get_subparsers(parser)
    args = parser.parse_args()
    args_list = (getattr(args, item) for item in dir(args) if not item.startswith('_'))
    subparsers_list = []
    seen = set()
    for item in args_list:
        if (isinstance(item, collections.Hashable) and item in subparsers
            and item not in seen):
            subparsers_list.append(item.replace('-', '_'))
            seen.add(item)
    cmd_func_name = 'cmd_' + '_'.join(subparsers_list)
    commands.__dict__[cmd_func_name](args)

if __name__ == '__main__':
    main()
