import argparse

parser = argparse.ArgumentParser(prog='moocx', description='EdX MOOC Data Anaylysis')
parser.add_argument('-v', '--version', action='version', version='0.1.0')

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List commands')
list_parser.add_argument('list_commands', action='store', choices=['all', 'basic'],help='List anayltics commands based on choice')

# An run command to execute the analysis
run_parser = subparsers.add_parser('run', help='Run commands')
run_parser.add_argument('run_commands', help='Run analytics based on argument', nargs='?', default='basic')

if __name__ == '__main__':
    args = parser.parse_args()
    print args
