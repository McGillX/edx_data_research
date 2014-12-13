'''

This module takes a list of collections to retrieve from the mongodb DATABASE_ADDRESS

Usage:

connection = EdXConnection('atoc185x', 'tracking', 'course_structure')
collection = connection.get_access_to_collection()
# collection now is a list of two elements, each element referring to the corresponding collection

'''

from pymongo import MongoClient

DATABASE_ADDRESS = "mongodb://localhost"


class EdXConnection(object):
    
    def __init__(self, db_name, *collections):
        client = MongoClient(DATABASE_ADDRESS)
        db = client[db_name]
        self.collections = {collection : db[collection] for collection in collections}

    def get_access_to_collection(self):
        return self.collections
