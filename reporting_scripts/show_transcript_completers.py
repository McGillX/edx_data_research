'''
This module retrieve the completers (users who completed the course)
and filters all those who had event_type 'show_transcript'
'''

import csv

from base_edx import EdXConnection

connection = EdXConnection('tracking')
collection = connection.get_access_to_collection()

with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    #usernames = [row[2] for row in reader]
    usernames = [row[2] for row in reader]


#cursor = collection['tracking'].aggregate([{"$match" : {"event_source" : "browser", "$or" : [{"event_type" : "seq_prev"},{"event_type" : "seq_goto"},{"event_type" : "seq_next"}], 'username' : {'$in' : usernames}}}, {"$group" : {"_id" : {'chapter_name' : "$parent_data.chapter_display_name", "display_name" :  "$metadata.display_name", "event_type"  : "$event_type", "event_old" : "$event.old", "event_new" : "$event.new"}, "count" : {"$sum" : 1}}}])

cursor = collection['tracking'].find({'event_type' : 'show_transcript'})

with open('csv_files/show_transcript_completers.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Username'])
    temp_set = set()
    for item in cursor:
        if item['username'] in usernames and item['username']  not in temp_set:
            temp_set.add(item['username'])
            writer.writerow([item['username']])
