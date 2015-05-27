import csv
import sys
import json

# These modules can be found under reporting scripts. You will have to add them
# in the same directory as this script
from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

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
output = dict()
for doc in student_answers_db:
    try:
        username = doc["username"]
        problem_id = doc['event']['problem_id']
        student_answers =  doc['event']['answers']
        student_attempts =  doc['event']['attempts']
        student_answers_values = dict()
        for key, values in student_answers.iteritems():
            if isinstance(values, list):
                if "choice_" in ",".join(values):
                    mapped_values = answer_keys[key].values()
                    student_answers_values[key] = mapped_values
                else:
                    student_answers_values[key] = values 
            else:
                if "choice_" in values:
                    mapped_values = answer_keys[key].values()
                    student_answers_values[key] = mapped_values
                else:
                    student_answers_values[key] = values
        if username not in output:
            output[username] = {'problem_id' : problem_id, 'student_answers' :  student_answers_values, 'attempts' : student_attempts}
        else: 
            if student_attempts > output[username]['attempts']:
                output[username]['problem_id'] = problem_id
                output[username]['student_answers'] = student_answers_values
                output[username]['attempts'] = student_attempts
    except:
        print "Key Error!!!", key, values, problem_id

result = []
for key, values in output.iteritems():
    username = key
    problem_id = values['problem_id']
    for question, answer in values['student_answers'].iteritems():
        result.append([username, problem_id, question, answer])
        
output = CSV(result, ['Username','Problem ID', 'Student Answers' ], output_file=db_name + '_student_answers.csv')
output.generate_csv()

#with open(db_name + '_student_answers', 'w') as f:
#    json.dump(output, f)
