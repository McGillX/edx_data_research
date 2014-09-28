'''
This module gets the number of students who answered a given problem correctly 
or incorrectly.

We first created a new collection user_attempts_per_problem_id to get the user
attempts for each problem id. The following aggregation query was used to create
the new collection:

db.tracking_atoc185x.aggregate([{$match : {event_type : 'problem_check', 'event_source': 'server'}}, {$group : {_id : {"username" : "$username", "problem_id" : "$event.problem_id"}, attempts : {$push : "$event.success"}}}, {$out : "user_attempts_per_problem_id"}])

Then run this script on the above collection

Usage:

python activities_with_lower_completion.py

'''
from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

# Connect to MongoDB and extra the tracking collection
connection = EdXConnection('user_attempts_per_problem_id')
collection = connection.get_access_to_collection()

cursor = collection['user_attempts_per_problem_id'].find()
result = defaultdict(lambda: defaultdict(int)) 
for index,document in enumerate(cursor):
    # If there is a correct attempts, accept as answered correctly, else accept
    #as incorrect only once per student per problem id
    if 'correct' in document['attempts']:
        result[document['_id']['problem_id']]['correct'] += 1
    else:
        result[document['_id']['problem_id']]['incorrect'] += 1

# Convert result to a 2D result to pass to CSV constructor from the module generate_csv_report
csv_result = [[item, result[item]['correct'], result[item]['incorrect']] for item in result]
#csv_result = [[item, result[item]['correct'], result['item']['incorrect']] for item in result]
output = CSV(csv_result, ['Problem Id', 'Correct Count', 'Incorrect Count'], output_file='activities_with_lower_completion.csv')
output.generate_csv()
