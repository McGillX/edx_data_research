import argparse
import inspect
import os
import sys

from edx_data_research.cli import commands

def main():
    parser = argparse.ArgumentParser(prog='moocx',
                                     description='EdX MOOC Data Anaylysis')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1.0')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # A list command
    list_parser = subparsers.add_parser('list', help='List commands')
    list_parser.add_argument(list_parser.prog.split(' ')[-1], action='store', choices=['all', 'basic'],
                              help='List anayltics commands based on choice')

    # An report command to execute the analysis and/or generate CSV reports
    report_parser = subparsers.add_parser('report', help='Report commands')
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
    report_subparsers = report_parser.add_subparsers(help='report', dest='report')
    basic_parser = report_subparsers.add_parser('basic', help='Run basic '
                                                'report generation commands')
    basic_parser.add_argument('basic', help='Run analytics based on argument')
    problem_ids_parser = report_subparsers.add_parser('problem-ids',
                                                     help='Generate CSV '
                                                     'reports for given problem ids')
                                                     
    problem_ids_parser.add_argument('problem_ids', nargs='+', help='Problem ID')
    problem_ids_parser.add_argument('-f', '--final-attempt', action='store_true',
                                   help="Only include students' final attempt "
                                   "to the given problem ids")

    args = parser.parse_args()
    attr = args.command
    cmd_func_name = ['cmd', attr]
    try:
        while attr:
            attr = getattr(args, attr)
            if isinstance(attr, basestring):
                attr = attr.replace('-', '_')
            cmd_func_name.append(attr)
    except (AttributeError, TypeError):
        pass
    cmd_func_name = '_'.join(cmd_func_name[:-1])
    commands.__dict__[cmd_func_name](args)

if __name__ == '__main__':
    main()
