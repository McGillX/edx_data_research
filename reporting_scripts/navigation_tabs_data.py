'''
This module gets the number of users who access each navigation tab
'''

import csv
from datetime import datetime
from collections import defaultdict
import sys

from base_edx import EdXConnection
fron generate_csv_report import CSV

# Connect to MongoDB and extra the tracking collection
connection = EdXConnection('tracking')
collection = connection.get_access_to_collection()

# User must hardcode navigation tabs for a given course
NAVIGATION_TABS = {'/courses/McGillX/CHEM181X/1T2014/info' : 'info', '/courses/McGillX/CHEM181X/1T2014/progress' : 'progress', '/courses/McGillX/CHEM181X/1T2014/c5f7240cf6d84cd4910ae5bc6d376b92/' : 'syllabus', '/courses/McGillX/CHEM181X/1T2014/ba5df4a4358b481b8d39101b5652d871/' : 'maps', '/courses/McGillX/CHEM181X/1T2014/7dfff8b7ef0046199fb5a2bc82b9080b/' : 'discussion_wrap_up', '/courses/McGillX/CHEM181X/1T2014/50eb3a7508344269acf0f77c60320ab8/' : 'food_movements', '/courses/McGillX/CHEM181X/1T2014/f976fd6a6c65405eb218f6ead3f785f/' : 'faq', 'courseware' : 'courseware', 'discussion': 'discussion'}

cursor = collection['tracking'].find({'event_type' : { '$regex' : '^/courses/McGillX/CHEM181x/1T2014/(info$|progress$|c5f7240cf6d84cd4910ae5bc6d376b92/$|ba5df4a4358b481b8d39101b5652d871/$|7dfff8b7ef0046199fb5a2bc82b9080b/$|50eb3a7508344269acf0f77c60320ab8/$|f976fd6a6c65405eb218f6ead3f785fc/$|courseware|discussion)'}})
unique_users_per_tab = defaultdict(set)
for doc in cursor:
    if 'courseware' in doc['event_type']:
        unique_users_per_tab['courseware'].add(doc['username'])
    elif 'discussion' in doc['event_type']:
        unique_users_per_tab['discussion'].add(doc['username'])
    else:
        unique_users_per_tab[doc['event_type']].add(doc['username'])
        
#with open('csv_files/number_of_unique_users_per_navigation_tab.csv', 'w') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['Navigation Tab', 'Number of Unique Users'])
#    for key in unique_users_per_tab:
#        writer.writerow([key, len(unique_users_per_tab[key])])
#with open('csv_files/users_per_navigation_tab.csv', 'w') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(['Navigation Tab','Tab', 'Number of Unique Users'])
#    for key in unique_users_per_tab:
#        writer.writerow([key,NAVIGATION_TABS[key] ,len(unique_users_per_tab[key])])

result = []
for key in unique_users_per_tab:
    result.append(key, NAVIGATION_TABS[key], len(unique_users_per_tab[key]))
    
output = CSV(result, ['Navigation Tab','Tab', 'Number of Unique Users'], output_file='number_of_unique_users_per_navigation_tab.csv')
