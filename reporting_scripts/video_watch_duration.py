'''
1) start by aggregating a new collection that includes the video interaction, page navigation and page close events for users sorted by username and time
db.tracking.aggregate([{ $limit : 30 },{$match:{$and:[{'event_source':'browser'},{$or:[{'event_type':'play_video'},{'event_type':'speed_change_video'},{'event_type':'seq_goto'}, {'event_type':'seq_next'}, {'event_type':'seq_prev'}, {'event_type':'page_close'}, {'event_type':'play_video'},{'event_type':'pause_video'}, {'event_type':'seek_video'}, {'event_type':'pause_video'}]}]}}, {$project:{"username":1, "event_type":1, 'time':1,"event":1}},{ $sort: {'username':1,'time':1}},{$out: "video_watching"}])
'''

import sys
#import csv
import time
from datetime import datetime

from base_edx import EdXConnection
#from generate_csv_report import CSV 

db_name = sys.argv[1]

eventCollection = 'video_watching'
connection = EdXConnection(db_name, eventCollection)
collection = connection.get_access_to_collection()



students = collection[eventCollection].distinct('username')
print
print students

watch_durations =[]
start_event_time = {'blank'}
end_event_time = {'blank'}

for student in students[0:2]:
    print
    print student
    cursor = collection[eventCollection].find({'username':student})
    #if play_video event then count as start
    for index,item in enumerate(cursor):
#if both a start and end event have been found append them to the list
        if start_event_time !={'blank'} and end_event_time != {'blank'}:
            watch_durations.append([student, video_id, start_event_time,end_event_time])
        if item['event_type'] == 'play_video':
            start_event_time = item['time']
            video_id = item['event']
            print 'start'
            print (start_event_time)
#when a start event is found set the end event to blank
            end_event_time = {'blank'}
            continue
        else:
            end_event_time = item['time']
            print 'end'
            print (end_event_time)
            continue
print watch_durations

            
