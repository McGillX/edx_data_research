'''
This module extracts all the videos watched and the problems attempted by users 
who got grades between 50% and 59% inclusive

Usage:

python failure_analysis.py

'''
# You will need csv module only if you are using the first method to extract
# usernames from the grades report csv file provided by edX
import csv

# Connect to MongoDB and extra the tracking collection
from base_edx import EdXConnection
from generate_csv_report import CSV 

# If you have access to the grade report provided by edX, you can use the following
# 7 lines of code to get all usernames with grades between 50% and 59% inclusive
#with open('csv_files/grades_report.csv') as f:
#    reader = csv.reader(f)
#    header = reader.next()
#    usernames = [row[2] for row in reader if '0.5' <= row[3] <= '0.59']
#connection = EdXConnection('tracking')
#collection = connection.get_access_to_collection()
#cursor = collection['tracking'].aggregate([{'$match' : {'username' : {'$in' : usernames}, '$or': [{'event_type' : 'play_video'},{'event_type' : 'problem_check', 'event_source' : 'server'}]}},{'$group' : { '_id' : { "username" : "$username", "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name","vertical_name" : "$parent_data.vertical_display_name"}}}, {'$out' : 'students_50_to_59_events'}])

# Else you can extract the names of the students with grades betweeb 50% and 59%
# inclusive from the collection certificates_generatedcertificate from the 
# following lines of code
connection = EdXConnection('tracking_atoc185x', 'auth_user', 'certificates_generatedcertificate')
collection = connection.get_access_to_collection()

# Get all user ids of students with grades between 50% and 59% inclusive from
# the collection certificates_generatedcertificate
user_ids = {document['user_id'] for document in collection['certificates_generatedcertificate'].find({'$and' : [{'grade' : {'$gte' : 0.5}},{'grade' : {'$lte' : 0.59}}]})}

# Get all the usernames corresponding to the user_ids you got from above
usernames = [document['username'] for document in collection['auth_user'].find() if document['id'] in user_ids]

# Extract all the videos watched and the problems attempted by users who got 
# grades between 50% and 59% inclusive
cursor = collection['tracking_atoc185x'].aggregate([{'$match' : {'username' : {'$in' : usernames}, '$or': [{'event_type' : 'play_video'},{'event_type' : 'problem_check', 'event_source'     : 'server'}]}},{'$group' : { '_id' : { "username" : "$username", "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name"    ,"vertical_name" : "$parent_data.vertical_display_name"}}}]) #, {'$out' : 'students_50_to_59_events'}]) 

result = [[document['_id']['username'], document['_id']['chapter_name'],document['_id']['sequential_name'],document['_id']['vertical_name']] for document in cursor['result'] if 'chapter_name' in document['_id']]
output = CSV(result, ['Username','Chapter Name' ,'Sequential Name' ,'Vertical Name'], output_file='failure_analysis_50_to_59.csv')
output.generate_csv()
