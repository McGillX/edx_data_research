import subprocess

from edx_data_research.parsing.parse import Parse

class Forum(Parse):

    def __init__(self, args):
        super(Forum, self).__init__(args)
        self._collections = 'forum'
        self.forum_file = args.forum_file

    def migrate(self):
        subprocess.check_call(['mongoimport', '-d', self.db_name, '-c',
                               self._collections, '--type', 'json', '--file',
                               self.forum_file, '--headerline', '--drop'])
