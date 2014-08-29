'''
This module keeps track of the number of times each Navigation tab was clicked/views, 
by students who completed the course, for each day during the course
'''

import csv
from datetime import datetime
from collections import defaultdict
import sys

from base_edx import EdXConnection

connection = EdXConnection('tracking')
collection = connection.get_access_to_collection()

# Get all users who completed the course
with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    usernames = [row[2] for row in reader]

NAVIGATION_TABS = {'/courses/McGillX/CHEM181X/1T2014/info' : 'info', '/courses/McGillX/CHEM181X/1T2014/progress' : 'progress', '/courses/McGillX/CHEM181X/1T2014/c5f7240cf6d84cd4910ae5bc6d376b92/' : 'syllabus', '/courses/McGillX/CHEM181X/1T2014/ba5df4a4358b481b8d39101b5652d871/' : 'maps', '/courses/McGillX/CHEM181X/1T2014/7dfff8b7ef0046199fb5a2bc82b9080b/' : 'discussion_wrap_up', '/courses/McGillX/CHEM181X/1T2014/50eb3a7508344269acf0f77c60320ab8/' : 'food_movements', '/courses/McGillX/CHEM181X/1T2014/f976fd6a6c65405eb218f6ead3f785f/' : 'faq', 'courseware' : 'courseware', 'discussion': 'discussion'}

# Filter for all students who completed the course and then aggregate the data for the navigation tabs
cursor = collection['tracking'].find({'username' : {'$in' : usernames},'event_type' : { '$regex' : '^/courses/McGillX/CHEM181x/1T2014/(info$|progress$|c5f7240cf6d84cd4910ae5bc6d376b92/$|ba5df4a4358b481b8d39101b5652d871/$|7dfff8b7ef0046199fb5a2bc82b9080b/$|50eb3a7508344269acf0f77c60320ab8/$|f976fd6a6c65405eb218f6ead3f785fc/$|courseware|discussion)'}})
tab_events_per_date = defaultdict(int)
for doc in cursor:
    date = datetime.strptime(doc['time'].split('T')[0], "%Y-%m-%d").date()
    if 'courseware' in doc['event_type']:
        tab_events_per_date[(date,'courseware')] += 1
    elif 'discussion' in doc['event_type']:
        tab_events_per_date[(date, 'discussion')] += 1
    else:
        tab_events_per_date[(date, doc['event_type'])] += 1
with open('csv_files/number_of_tab_events_per_date_completers.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Date','Tab ID','Number of Events'])
    for date,tab in tab_events_per_date:
        writer.writerow([date,tab, tab_events_per_date[(date,tab)] ])
