'''
This module extracts the student IDs from the collection certificates_generatedcertificate
of the students who completed the course and achieved a certificate. The ids
are then used to extract the usernames of the course completers

Usage:

python course_completers.py

'''

from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('certificates_generatedcertificate', 'auth_user')
collection = connection.get_access_to_collection()

completers = collection['certificates_generatedcertificate'].find({'status' : 'downloadable'})

result = []
for document in completers:
    user_document = collection['auth_user'].find_one({"id" : document['user_id']})
    result.append([user_document['username'], document['name'], document['grade']])

output = CSV(result, ['Username', 'Name', 'Grade'], output_file='course_completers.csv')
output.generate_csv()
