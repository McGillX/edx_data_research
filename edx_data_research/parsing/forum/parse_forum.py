import subprocess

from edx_data_research.parsing.edx_parse import EdXParse

class Forum(EdXParse):

    def __init__(self, args):
        super(Forum, self).__init__(args)
        self._collections = args.collection
        self.forum_file = args.forum_file

    def migrate(self):
        subprocess.check_call(['mongoimport', '-d', self.db_name, '-c',
                               self._collections, '--type', 'json', '--file',
                               self.forum_file, '--headerline'])
