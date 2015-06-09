'''
This module retrieve the first activity of all user who completed a course
The list of users who has completed the course was provided in a given csv file,
McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv. When these users are
extracted, we then check the database for all of these users and detect their 
first activity. First activity is defined by the event_type '/courses/McGillX/CHEM181x/1T2014/info'

'''
import csv
from datetime import datetime
from collections import defaultdict


from common.base_edx import EdXConnection

# Connect to MongoDB and extra the tracking collection
connection = EdXConnection('tracking', 'tracking_before_jan22')
collection = connection.get_access_to_collection()

# Retrieve users who has completed the course. This could be done anyway depending on what is provided
with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    #usernames = [row[2] for row in reader]
    usernames = [row[2] for row in reader]

# Retrieve the time of the first activity of all users who completed the course
time_events = defaultdict(list)
cursor = collection['tracking'].find({'event_type' : '/courses/McGillX/CHEM181x/1T2014/info'})
#cursor_before_jan_22 = collection['tracking_before_jan22'].find({'event_type' : '/courses/McGillX/CHEM181x/1T2014/info'})
with open('csv_files/first_activity_completers.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Username', 'Date of Registration'])
    temp_set = set()
    for item in cursor:
        if item['username'] in usernames:
            time_events[item['username']].append(item['time'])
    for key in time_events:
        writer.writerow([key, datetime.strptime(min(time_events[key]).split('T')[0], "%Y-%m-%d").date()])
