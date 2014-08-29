'''
This module gets the number of students who answered a given problem correctly or incorrectly
'''
from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

# Connect to MongoDB and extra the tracking collection
connection = EdXConnection('user_attempts')
collection = connection.get_access_to_collection()

cursor = collection['user_attempts'].find()
result = defaultdict(lambda: defaultdict(int)) 
for index,document in enumerate(cursor):
    if len(document['_id']) > 2: 
        if 'correct' in document['attempts']:
            result[(document['_id']['chapter_name'], document['_id']['sequential_name'],document['_id']['vertical_name'],document['_id']['problem_id'])]['correct'] += 1
        else:
            result[(document['_id']['chapter_name'], document['_id']['sequential_name'],document['_id']['vertical_name'],document['_id']['problem_id'])]['incorrect'] += 1

# Convert result to a 2D result to pass to CSV constructor from the module generate_csv_report
csv_result = []
for item in result:
    csv_result.append(list(item) + [result[item]['correct'], result[item]['incorrect']])

output = CSV(csv_result, ['Chapter Name', 'Sequential Name', 'Vertical Name', 'Problem Id', 'Correct Count', 'Incorrect Count'], output_file='activities_with_lower_completion.csv')
output.generate_csv()
