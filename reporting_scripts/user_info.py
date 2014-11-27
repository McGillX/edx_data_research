'''
This module will retrieve info about students registered in the course

Usage:

python user_info.py

'''

from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV 

connection = EdXConnection('certificates_generatedcertificate', 'auth_userprofile')
collection = connection.get_access_to_collection()

documents = collection['auth_userprofile'].find()

result = []

for document in documents:
    user_id = document['user_id']
    try:
        final_grade = collection['certificates_generatedcertificate'].find_one({'user_id' : user_id})['grade']
        result.append([user_id, document['name'], final_grade, document['gender'], document['year_of_birth'], document['level_of_education'], document['country'], document['city']])
    except:
        # Handle users with no grades
        pass
    
output = CSV(result, ['User ID','Username', 'Final Grade', 'Gender', 'Year of Birth', 'Level of Education', 'Country', 'City'], output_file='atoc185x_user_info.csv')
output.generate_csv()
