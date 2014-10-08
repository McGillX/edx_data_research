'''
This module keeps track of the number of times each Navigation tab was clicked/views, 
by students who completed the course, for each day during the course

Usage:

python navigation_tabs_data_date.py 

'''

import csv
from datetime import datetime
from collections import defaultdict
import sys

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('tracking_atoc185x')
collection = connection.get_access_to_collection()

# Get all users who completed the course. If you do not have a CSV with list
# of users who had completed the course, you will have to extra it from the 
# MongoDB database
with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    usernames = [row[2] for row in reader]

NAVIGATION_TABS = {'/courses/McGillX/ATOC185x/2T2014/info' : 'info', '/courses/McGillX/ATOC185x/2T2014/progress' : 'progress', '/courses/McGillX/ATOC185x/2T2014/109d5374b52040e2a8b737cf90c5618a/' : 'syllabus', '/courses/McGillX/ATOC185x/2T2014/441b2c519f5c464883e2ddceb26c5559/' : 'maps','/courses/McGillX/ATOC185x/2T2014/84f630e833eb4dbabe0a6c45c52bb443/' : 'scoreboard' , '/courses/McGillX/ATOC185x/2T2014/e75195cb39fa4e3890a613a1b3c04c7d/' : 'faq', 'courseware' : 'courseware', 'discussion': 'discussion', '/courses/McGillX/ATOC185x/2T2014/instructor' : 'instructor'}

cursor = collection['tracking_atoc185x'].find({'username' : {'$in' : usernames},'event_type' : { '$regex' : '^/courses/McGillX/ATOC185x/2T2014/(info$|progress$|instructor$|109d5374b52040e2a8b737cf90c5618a/$|441b2c519f5c464883e2ddceb26c5559/$|84f630e833eb4dbabe0a6c45c52bb443/$|e75195cb39fa4e3890a613a1b3c04c7d/$|courseware|discussion)'}})

tab_events_per_date = defaultdict(int)
for doc in cursor:
    date = datetime.strptime(doc['time'].split('T')[0], "%Y-%m-%d").date()
    if 'courseware' in doc['event_type']:
        tab_events_per_date[(date,'courseware')] += 1
    elif 'discussion' in doc['event_type']:
        tab_events_per_date[(date, 'discussion')] += 1
    else:
        tab_events_per_date[(date, doc['event_type'])] += 1

result = []
for date, tab in tab_events_per_date:
    result.append([date,tab, tab_events_per_date[(date,tab)]])
output = CSV(result, ['Date','Tab ID','Number of Events'], output_file='number_of_tab_events_per_date_completers.csv')
output.generate_csv()

#with open('csv_files/number_of_tab_events_per_date_completers.csv', 'w') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['Date','Tab ID','Number of Events'])
#    for date,tab in tab_events_per_date:
#        writer.writerow([date,tab, tab_events_per_date[(date,tab)] ])
