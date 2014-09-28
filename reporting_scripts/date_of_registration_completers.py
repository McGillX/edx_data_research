'''
This module gets the date of registration of all users who completed the course

Usage:

python date_of_registration_completers.py 

'''

import csv
from datetime import datetime

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('tracking_atoc185x')
collection = connection.get_access_to_collection()

# Can replace csv file with any csv file that contains the list of usernames 
# who completed the course and achieved a certificate. Alternately, one can
# save that info in another collection in mongoDB and extra it from the collection
with open('atoc185x/course_completers.csv') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    usernames = { row[0] for row in reader }

result = []
tracking = collection['tracking_atoc185x'].find({'event_type' : 'edx.course.enrollment.activated'})
seen = set()
for document in  tracking:
    if document['username'] in usernames and document['username'] not in seen:
        seen.add(document['username'])
        result.append([document['username'],datetime.strptime(document['time'].split('T')[0], "%Y-%m-%d").date()])

output = CSV(result, ['Username', 'Date of Registration'], output_file='date_of_registration_completers.csv')
output.generate_csv()
