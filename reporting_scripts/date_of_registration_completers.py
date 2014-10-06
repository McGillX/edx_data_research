'''
This module gets the date of registration of all users who completed the course

Usage:

python date_of_registration_completers.py 

'''

import csv
from datetime import datetime

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('student_courseenrollment')
collection = connection.get_access_to_collection()

# Can replace csv file with any csv file that contains the list of usernames 
# who completed the course and achieved a certificate. Alternately, one can
# save that info in another collection in mongoDB and extra it from the collection
with open('atoc185x/course_completers.csv') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    users = { row[0] : row[1] for row in reader }

result = []
student_courseenrollment = collection['student_courseenrollment'].find()
seen = set()
for document in  student_courseenrollment:
    if str(document['user_id']) in users and document['user_id'] not in seen:
        seen.add(document['user_id'])
        result.append([document['user_id'], users[str(document['user_id'])],document['created'].split()[0]]) 

output = CSV(result, ['Username', 'Date of Registration'], output_file='date_of_registration_completers.csv')
output.generate_csv()
