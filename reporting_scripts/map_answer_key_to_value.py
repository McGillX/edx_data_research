import csv
import sys

from collections import defaultdict

# These modules can be found under reporting scripts. You will have to add them
# in the same directory as this script
from base_edx import EdXConnection
from generate_csv_report import CSV

db_name = sys.argv[1]
answer_distribution = sys.argv[2]
connection = EdXConnection(db_name, 'tracking' )
collection = connection.get_access_to_collection()

with open(answer_distribution) as f:
    csv_f = csv.reader(f)
    headers = csv_f.next()
    rows = [row for row in csv_f]

answer_keys = dict()

for row in rows:
    problem_id = row[1]
    value = row[4]
    answer_value = row[5]
    if value:
        value = value.replace('[', '').replace(']', '').split('|')
        answer_value = answer_value.replace('[', '').replace(']', '').split('|')
        dict_value_answer = dict(zip(value, answer_value))
        try:
            answer_keys[problem_id].update(dict_value_answer)
        except:
            answer_keys[problem_id] = dict_value_answer
         
student_answers_db = collection['tracking'].find({'event_type': 'problem_check', 'event_source' : 'server'})
for doc in student_answers_db:
    try:
        print doc['event']['state']['student_answers']
    except:
        print "Key Error!!!"
