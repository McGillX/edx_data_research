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
    '''
    MongoDB does not accept '$' as key values. Loop through all the jeys and
    remove the '$' symbol

    '''
    for key in json_object.keys():
        if isinstance(json_object[key], dict):
            for item in json_object[key].keys():
                new_key = item.replace('$', '')
                if new_key != item:
                    json_object[key][new_key] = json_object[key][item]
                    del json_data[key][item]
        # Some values inside the object are 'parent_ids':[{'$oid': u'52e0082cfbd06391ba0000a4'}]
        # The [{}] will trigger an error in MongoDB (not 100% sure)
        # Here, [] and '$' are filtered out
        if isinstance(json_data[key], list) and len(json_data[json_object[key]]) == 1 and isinstance(json_object[key][0], dict):
            for item in json_data[key][0].keys():
                new_key = item.replace('$', '')
                if new_key != item:
                    temp_value = json_data[key][0][item]
                    del json_object[key]
                    json_object[key] = {new_key : temp_value}
    return json_object


def migrate_form_to_mongodb(forum_mongo_file, collection):
    with open(forum_mongo_file) as file_handler:
        try:
            for line in file_handler:
                data = json.loads(line)
                data = remove_dollar_sign(data)
                collection.insert(data)
        except pymongo.errors.InvalidDocument as e:
            print "INVALID_DOC: ", line
        except Exception as e:
            print "ERROR: ", line


def main():
    if len(sys.argv) != 4:
        usage_message = 'usage: %s coure_db_name forum_mongo_file'

if __name__ == '__main__':
    main()
