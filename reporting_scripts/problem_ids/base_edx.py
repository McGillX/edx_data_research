'''

This module takes a list of collections to retrieve from the mongodb DATABASE_ADDRESS

Usage:

connection = EdXConnection('tracking', 'course_structure')
collection = connection.get_access_to_collection()
# collection now is a list of two elements, each element referring to the corresponding collection

'''

from pymongo import MongoClient

DATABASE_ADDRESS = "mongodb://localhost"
# Make sure to change name of database before running the reporting scripts
DATABASE_NAME = 'atoc185x'

class EdXConnection(object):
    
    def __init__(self,*collections):
        client = MongoClient(DATABASE_ADDRESS)
        db = client[DATABASE_NAME]
        self.collection = {collection : db[collection] for collection in collections}

    def get_access_to_collection(self):
        return self.collection
