'''
This module keeps track of the number of times each Navigation tab was clicked/views 
for each day during the course
'''
#import csv
from datetime import datetime
from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('tracking_atoc185x')
collection = connection.get_access_to_collection()

# User will need to hardcode the names of the navigation tabs for a given course
#NAVIGATION_TABS = {'/courses/McGillX/CHEM181X/1T2014/info' : 'info', '/courses/McGillX/CHEM181X/1T2014/progress' : 'progress', '/courses/McGillX/CHEM181X/1T2014/c5f7240cf6d84cd4910ae5bc6d376b92/' : 'syllabus', '/courses/McGillX/CHEM181X/1T2014/ba5df4a4358b481b8d39101b5652d871/' : 'maps', '/courses/McGillX/CHEM181X/1T2014/7dfff8b7ef0046199fb5a2bc82b9080b/' : 'discussion_wrap_up', '/courses/McGillX/CHEM181X/1T2014/50eb3a7508344269acf0f77c60320ab8/' : 'food_movements', '/courses/McGillX/CHEM181X/1T2014/f976fd6a6c65405eb218f6ead3f785f/' : 'faq', 'courseware' : 'courseware', 'discussion': 'discussion'}

NAVIGATION_TABS = {'/courses/McGillX/ATOC185x/2T2014/info' : 'info', '/courses/McGillX/ATOC185x/2T2014/progress' : 'progress', '/courses/McGillX/ATOC185x/2T2014/109d5374b52040e2a8b737cf90c5618a/' : 'syllabus', '/courses/McGillX/ATOC185x/2T2014/441b2c519f5c464883e2ddceb26c5559/' : 'maps','/courses/McGillX/ATOC185x/2T2014/84f630e833eb4dbabe0a6c45c52bb443/' : 'scoreboard' , '/courses/McGillX/ATOC185x/2T2014/e75195cb39fa4e3890a613a1b3c04c7d/' : 'faq', 'courseware' : 'courseware', 'discussion': 'discussion', '/courses/McGillX/ATOC185x/2T2014/instructor' : 'instructor'}

cursor = collection['tracking_atoc185x'].find({'event_type' : { '$regex' : '^/courses/McGillX/ATOC185x/2T2014/(info$|progress$|instructor$|109d5374b52040e2a8b737cf90c5618a/$|441b2c519f5c464883e2ddceb26c5559/$|84f630e833eb4dbabe0a6c45c52bb443/$|e75195cb39fa4e3890a613a1b3c04c7d/$|courseware|discussion)'}})

tab_events_per_date = defaultdict(int)
for doc in cursor:
    date = datetime.strptime(doc['time'].split('T')[0], "%Y-%m-%d").date()
    if 'courseware' in doc['event_type']:
        tab_events_per_date[(date,'courseware')] += 1
    elif 'discussion' in doc['event_type']:
        tab_events_per_date[(date, 'discussion')] += 1
    else:
        tab_events_per_date[(date, doc['event_type'])] += 1

#with open('csv_files/number_of_tab_events_per_date.csv', 'w') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['Date','Tab ID','Number of Events'])
#    for date,tab in tab_events_per_date:
#        writer.writerow([date,tab, tab_events_per_date[(date,tab)] ])

result = []
for date,tab in tab_events_per_date:
    result.append([date,tab, tab_events_per_date[(date,tab)] ])

output = CSV(result, ['Date','Tab ID','Number of Events'], output_file='number_of_tab_events_per_date.csv')
output.generate_csv()
