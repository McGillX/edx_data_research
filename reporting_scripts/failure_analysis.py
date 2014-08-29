'''
This module extracts all the videos watched and the problems attempted by users 
who got grades between 50% and 59%
'''

import csv
from collections import defaultdict
from datetime import datetime

# Connect to MongoDB and extra the tracking collection
from base_edx import EdXConnection
from generate_csv_report import CSV 

with open('csv_files/grades_report.csv') as f:
    reader = csv.reader(f)
    header = reader.next()
    usernames = [row[2] for row in reader if '0.5' <= row[3] <= '0.59']

connection = EdXConnection('tracking')
collection = connection.get_access_to_collection()
cursor = collection['tracking'].aggregate([{'$match' : {'username' : {'$in' : usernames}, '$or': [{'event_type' : 'play_video'},{'event_type' : 'problem_check', 'event_source' : 'server'}]}},{'$group' : { '_id' : { "username" : "$username", "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name","vertical_name" : "$parent_data.vertical_display_name"}}}, {'$out' : 'students_50_to_59_events'}])

