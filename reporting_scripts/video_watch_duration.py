'''
1) start by aggregating a new collection that includes the video interaction, page navigation and page close events for users sorted by username and time
db.tracking.aggregate([{$match:{$and:[{'event_source':'browser'},{$or:[{'event_type':'play_video'},{'event_type':'speed_change_video'},{'event_type':'seq_goto'}, {'event_type':'seq_next'}, {'event_type':'seq_prev'}, {'event_type':'page_close'}, {'event_type':'play_video'},{'event_type':'pause_video'}, {'event_type':'seek_video'}, {'event_type':'pause_video'}]}]}}, {$project:{"username":1, "event_type":1, 'time':1,"event":1}},{ $sort: {'username':1,'time':1}},{$out: "video_watching"}],{allowDiskUse:true})
or
db.runCommand({aggregate:'tracking',pipeline:[{$match:{$and:[{'event_source':'browser'},{$or:[{'event_type':'play_video'},{'event_type':'speed_change_video'},{'event_type':'seq_goto'}, {'event_type':'seq_next'}, {'event_type':'seq_prev'}, {'event_type':'page_close'}, {'event_type':'play_video'},{'event_type':'pause_video'}, {'event_type':'seek_video'}, {'event_type':'pause_video'}]}]}}, {$project:{"username":1, "event_type":1, 'time':1,"event":1}},{ $sort: {'username':1,'time':1}},{$out: "video_watching"}],allowDiskUse:true})
'''
import sys
import csv
import time
from datetime import datetime

from base_edx import EdXConnection
from generate_csv_report import CSV 

db_name = sys.argv[1]

eventCollection = 'video_watching'
connection = EdXConnection(db_name, eventCollection)
collection = connection.get_access_to_collection()



students = collection[eventCollection].distinct('username')
print
print students
print len(students)

watch_durations =[]
start_event_time = {'blank'}
end_event_time = {'blank'}
errors = []
count_errors = 0

for student in students:
    cursor = collection[eventCollection].find({'username':student})
    #if play_video event then count as start
    for index,item in enumerate(cursor):
        try:
    #if both a start and end event have been found append them to the list
            if start_event_time !={'blank'} and end_event_time != {'blank'}:
                duration = end_event_time - start_event_time
    #append all the values for a given watch_duration to the watch_durations list
                watch_durations.append([student, video_id, video_code, time_point, start_event_time,end_event_time,duration])
                start_event_time = {'blank'}
                end_event_time = {'blank'}
    #if event is play_video then assign as start
            if item['event_type'] == 'play_video':
                start_event_time = datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
    #get values related to video identification
                video = item['event']
                video_code = video['code']
                video_id = video['id']
                time_point = video['currentTime']
                print 'start'
                print (start_event_time)
    #when a start event is found set the end event to blank
                end_event_time = {'blank'}
                continue
    #assign all other event types to end
    #Note: currently seek_video events count as an end_event
            else:
                end_event_time = datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
                print 'end'
                print (end_event_time)
                continue
        except:
            count_errors = count_errors+1
            errors.append([index,item])
#print watch_durations
print 
print len(watch_durations)
print errors
output = CSV(watch_durations, ['Username','video_id','youtube id (video_code)','time_point (seconds)','start_event_time','end_event_time', 'duration (minutes)'], output_file=db_name+'video_watch_duration.csv', row_limit=200000) 
output.generate_csv()
output_errors = CSV(errors, ['Errors'], output_file=db_name+'video_watch_duration_errors.csv', row_limit=200000)
output_errors.generate_csv()
