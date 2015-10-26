import subprocess

from pymongo import MongoClient

class SQL(object):

    def __init__(self, args):
        self.uri = args.uri
        client = MongoClient(self.uri)
        self._db = client[args.db_name]
        self._collections = args.collection
        self.sql_file = args.sql_file

    def migrate(self):
        subprocess.check_call(['mongoimport', '-d', self._db.name, '-c',
                               self._collections, '--type', 'tsv', '--file',
                               self.sql_file, '--headerline'])
