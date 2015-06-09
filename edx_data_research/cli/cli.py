import argparse
import inspect
import os
import sys

from edx_data_research.cli import commands

def main():
    parser = argparse.ArgumentParser(prog='moocx', description='EdX MOOC Data Anaylysis')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # A list command
    list_parser = subparsers.add_parser('list', help='List commands')
    list_parser.add_argument('action', action='store', choices=['all', 'basic'],help='List anayltics commands based on choice')

    # An run command to execute the analysis
    run_parser = subparsers.add_parser('run', help='Run commands')
    run_parser.add_argument('action', help='Run analytics based on argument', nargs='?', default='basic')
    run_parser.add_argument('db_name', help='Name of database where each database corresponds to a course offering')
    run_parser.add_argument('-u', '--uri', help='URI to MongoDB database (default: mongodb://localhost:27017)')
    run_parser.add_argument('-o', '--output', help='Path to directory to save CSV report (defaults to current directory: %(default)s)', default=os.getcwd(), dest='output_directory')
    run_parser.add_argument('-j', '--json', help='Path to JSON file that may be needed for some analytics commands')
    run_parser.add_argument('-c', '--csv', help='Path to CSV file that may be needed for some analytics commands')
    run_parser.add_argument('-p', '--problem-id', help='Course specifc problem ID that may be needed for some analytics commands', dest='problem_id')
    run_parser.add_argument('-r', '--row-limit', help='Number of rows per CSV file (default: %(default)s)', type=int, default=100000, dest='row_limit')

    args = parser.parse_args()
    commands.__dict__['cmd_'+ args.command + '_' + args.action.replace('-', '_')](args)

if __name__ == '__main__':
    main()
