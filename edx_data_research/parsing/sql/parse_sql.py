import subprocess

from edx_data_research.parsing.edx_parse import EdXParse

class SQL(EdXParse):

    def __init__(self, args):
        super(SQL, self).__init__(args)
        self._collections = args.collection
        self.sql_file = args.sql_file

    def migrate(self):
        subprocess.check_call(['mongoimport', '-d', self.db_name, '-c',
                               self._collections, '--type', 'tsv', '--file',
                               self.sql_file, '--headerline'])
