'''
This module aims to create a new collection which will have data relevant to
all the problem ids in a course whether they are homework assignment questions
or questions in the acitivities of a lecture

Creating a new collection with information only about problem ids and students
answers to those problem ids will allow us and others to focus on analysis
only on problem ids; hence the time taken to run queries on the data can be 
relatively less because we run these queries on only a subset of the tracking logs

Usage:

python -m problem_ids.create_problem_ids_collection.py <db_name> 

'''
from common.base_edx import EdXConnection
import sys

db_name = sys.argv[1]

# The second argument in line 27 is the name of the new collection which will 
# contain the results of this script. Each new document will be inserted into
# this new collection. The name of the resulting collection could be anything;
# preferrably relevant to the course
connection = EdXConnection(db_name, 'test1', 'tracking', 'user_id_map', 'problem_ids')
collection = connection.get_access_to_collection()

# Drop problem_ids collection if exists
collection['problem_ids'].drop()

cursor = collection['tracking'].find({'event_type' : 'problem_check', 'event_source' : 'server'})
for document in cursor:
    doc_result = {}
    username = document['username']
    if username.isdigit():
        username = int(username)
    doc_result['username'] = username
    user_id_map = collection['user_id_map'].find_one({'username' : username})
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
