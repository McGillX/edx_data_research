import argparse

parser = argparse.ArgumentParser(prog='moocx', description='EdX MOOC Data Anaylysis')
parser.add_argument('-v', '--version', action='version', version='0.1.0')

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List commands')
list_parser.add_argument('list_commands', action='store', choices=['all', 'basic'],help='List anayltics commands based on choice')

parser.parse_args()
