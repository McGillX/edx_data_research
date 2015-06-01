from pymongo import MongoClient

class BaseEdX(object):

    def __init__(self, args):
        self.url = args.url
        client = MongoClient(self.url)
        self.db = client[args.db_name]
        self.collections = None
        self.output_directory = args.output_directory
        self.row_limit = args.row_limit
        self.csv_data = None
        self.list_of_headers = None
