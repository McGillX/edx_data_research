import argparse
import os

def main():
    parser = argparse.ArgumentParser(prog='moocx', description='EdX MOOC Data Anaylysis')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')

    subparsers = parser.add_subparsers(help='commands')

    # A list command
    list_parser = subparsers.add_parser('list', help='List commands')
    list_parser.add_argument('list_action', action='store', choices=['all', 'basic'],help='List anayltics commands based on choice')

    # An run command to execute the analysis
    run_parser = subparsers.add_parser('run', help='Run commands')
    run_parser.add_argument('db_name', help='Name of database where each database corresponds to a course offering')
    run_parser.add_argument('run_action', help='Run analytics based on argument', nargs='?', default='basic')
    run_parser.add_argument('-o', '--output', help='Path to directory to save CSV report (defaults to current directory: %(default)s)', default=os.getcwd())
    run_parser.add_argument('-j', '--json', help='Path to JSON file that may be needed for some analytics commands')
    run_parser.add_argument('-c', '--csv', help='Path to CSV file that may be needed for some analytics commands')
    run_parser.add_argument('-p', '--problem-id', help='Course specifc problem ID that may be needed for some analytics commands')

    args = parser.parse_args()
    print args

if __name__ == '__main__':
    main()
