import json
import pymongo
import sys


def connect_to_db_collection(db_name, collection_name):
    '''
    Return collection of a given database name and collection name
    
    '''
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    collection = db[collection_name]
    return collection



def main():
    if len(sys.argv) !=  2:
        usage_message = """
        usage: %s db_name
        Create problem_ids collection\n 
        """
        sys.stderr.write(usage_message % sys.argv[0])
        sys.exit(1)
    problem_ids_collection = connect_to_db_collection(source_db, 'problem_ids')
    problem_ids_collection.drop()
    tracking_collection = connect_to_db_collection(source_db, 'tracking')
    user_id_map_collection = connect_to_db_collection(source_db, 'user_id_map')
    cursor = tracking_collection.find({'event_type' : 'problem_check',
                                       'event_source' : 'server'})
    for document in cursor:
        doc_result = {}
        username = document['username']
        if username.isdigit():
            username = int(username)
        doc_result['username'] = username
        user_id_map = user_id_map_collection.find_one({'username' : username})
        if not user_id_map:
            print "Username {0} not found in collection user_id_map".format(username)
            continue
        doc_result['user_id'] = user_id_map['id']
        doc_result['hash_id'] = user_id_map['hash_id']
        doc_result['problem_id'] = document['event']['problem_id']
        doc_result['course_id'] = document['context']['course_id']
        doc_result['module'] = document['context']['module']
        doc_result['time'] = document['time']
        doc_result['event'] = document['event']
        collection['problem_ids'].insert(doc_result)

if __name__ == '__main__':
    main()
