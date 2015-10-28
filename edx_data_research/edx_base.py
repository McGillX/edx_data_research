from pymongo import MongoClient


class EdX(object):

    def __init__(self, args):
        self.uri = args.uri
        self.db_name = args.db_name
        client = MongoClient(self.uri)
        self.db = client[self.db_name]
        self._collections = None

    @property
    def collections(self):
    	return self._collections
    	
    @collections.setter
    def collections(self, _collections):
    	self._collections = {collection : self.db[collection]
                             for collection in _collections}

