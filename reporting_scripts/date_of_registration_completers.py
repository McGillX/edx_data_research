'''
This module gets the date of registration of all users who completed the course
'''

import csv
from datetime import datetime

from base_edx import EdXConnection

connection = EdXConnection('tracking', 'tracking_before_jan22')
collection = connection.get_access_to_collection()

with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    #usernames = [row[2] for row in reader]
    usernames = [row[2] for row in reader]

cursor = collection['tracking'].find({'event_type' : 'edx.course.enrollment.activated'})
cursor_before_jan_22 = collection['tracking_before_jan22'].find({'event_type' : 'edx.course.enrollment.activated'})
with open('csv_files/date_of_registration_completers.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Username', 'Date of Registration'])
    temp_set = set()
    for item in cursor_before_jan_22:
        if item['username'] in usernames and item['username']  not in temp_set:
            temp_set.add(item['username'])
            writer.writerow([item['username'],datetime.strptime(item['time'].split('T')[0], "%Y-%m-%d").date()])
    for item in cursor:
        if item['username'] in usernames and item['username']  not in temp_set:
            temp_set.add(item['username'])
            writer.writerow([item['username'],datetime.strptime(item['time'].split('T')[0], "%Y-%m-%d").date()])
    for item in set(usernames) - temp_set:
        writer.writerow([item, datetime.strptime('2013-12-02', "%Y-%m-%d").date()])
