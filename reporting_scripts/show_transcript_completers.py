'''
This module retrieve the completers (users who completed the course)
and filters all those who had event_type 'show_transcript'

Usage:

python show_transcript_completers.py

'''

import csv

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

connection = EdXConnection('tracking_atoc185x')
collection = connection.get_access_to_collection()

# Can replace csv file with any csv file that contains the list of usernames 
# who completed the course and achieved a certificate. Alternately, one can
# save that info in another collection in mongoDB and extra it from the collection
with open('atoc185x/course_completers.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    usernames = {row[1] for row in reader}

cursor = collection['tracking_atoc185x'].find({'event_type' : 'show_transcript'})
result = []
seen = set()
for document in cursor:
    if document['username'] in usernames and document['username'] not in seen:
        seen.add(document['username'])
        result.append([document['username']])
output = CSV(result, ['Username'], output_file='show_transcript_completers.csv')
output.generate_csv()
