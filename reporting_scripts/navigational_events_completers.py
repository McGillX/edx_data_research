'''
This module counts the number of navigation events: seq_next, seq_prev, seq_goto
for those students who completed the course
'''

import csv

from base_edx import EdXConnection

connection = EdXConnection('tracking')
collection = connection.get_access_to_collection()

with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    usernames = [row[2] for row in reader]


cursor = collection['tracking'].aggregate([{"$match" : {"event_source" : "browser", "$or" : [{"event_type" : "seq_prev"},{"event_type" : "seq_goto"},{"event_type" : "seq_next"}], 'username' : {'$in' : usernames}}}, {"$group" : {"_id" : {'chapter_name' : "$parent_data.chapter_display_name", "display_name" :  "$metadata.display_name", "event_type"  : "$event_type", "event_old" : "$event.old", "event_new" : "$event.new"}, "count" : {"$sum" : 1}}}])

with open('csv_files/navigation_frequency_completers.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Chapter Name', 'Display Name', 'Event Type', 'Event Old', 'Event New', 'Count'])
    for item in cursor['result']:
        try:
            writer.writerow([item['_id']['chapter_name'], item['_id']['display_name'], item['_id']['event_type'], item['_id'].get('event_old', 0), item['_id']['event_new'], item['count']])
        except:
           pass 
