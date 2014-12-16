'''
Insert the edx discussion board .mongo files into mongodb database
'''

import pymongo
import sys
import json


def connect_to_db_collection(db_name, collection_name):
    '''
    Retrieve collection from given database name and collection name

    '''
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    collection = db[collection_name]
    return collection


def remove_dollar_sign(json_object):
    pass


def migrate_form_to_mongodb(forum_mongo_file, collection):
    pass

def main():
    if len(sys.argv) != 4:
        usage_message = 'usage: %s coure_db_name forum_mongo_file'

if __name__ == '__main__':
    main()
