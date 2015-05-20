'''

1) Create a new collection in the mongo shell:

db.tracking_collection.aggregate([{$match :{$or : [{"event_type" : "load_video"},{"event_type" : "seek_video"}, {"event_type" : "play_video"},{"event_type":"pause_video"}]}}, {$out : "video_watch_duration_collection"}])

2) Run: python video_watch_segments.py


desired final output.csv

new row for every unique load_video event for a username

username, video associated with load_video event, parent_data: {chapter_display_name, sequential_display_name, vertical_display_name,}, edx_video_id, video watch segments

get the event_types : load_video, play_video, pause_video, seek_video

sort by "time": "" so that the events are chronologically ordered

for each load_video new video watch segment should include ONLY:

- time between play_video -> next video event in time (pause_video or seek_video)
- time between seek_video : {'new_time' : Time}  -> pause video (only with new_time > old_time, this is to avoid including rewinds)

watch periods:
    event_type : pause_video - "event_type":"play_video" {"event":{"currentTime":TIME}} = new video watch segment
    if seek_video : {'old_time' : TIME} < seek_video : {'new_time' : TIME} 
      "pause_video" {"event":{"currentTime":TIME}} - seek_video : {'new_time': TIME } = new video watch segment

    if seek_video : {'old_time' : TIME} > seek_video : {'new_time' : TIME} = rewind (exclude from watch segments)
    
Notes:
Do not use session key from logs, only ends when student's log out
    
'''
import sys
#import csv
import time
from datetime import datetime

from base_edx import EdXConnection
#from generate_csv_report import CSV 

db_name = sys.argv[1]

connection = EdXConnection(db_name,'tracking')
collection = connection.get_access_to_collection()
result = []
#get all usernames
usernames = collection['tracking'].distinct('username')
print
print usernames

'''
for session_username in usernames
    documents = collection['tracking'].find({'username': session_username}).sort({"time": 1})
    for document in documents:
        session_start_time = document['event_type':'play_video','event_source':'browser','event.currentTime':0']
    session = collection['tracking'].find_one({'username': session_username, event_type':'play_video','event_source':'browser','event.currentTime':0})
    session_start_time = session['time']
    
'''
#restricting event_source to browser, excluding mobile events
session = collection['tracking'].find_one({'event_type':'play_video','event_source':'browser','event.currentTime':0})
print
print session

#get video id associated with session
#video_id= session['id']

video_page = session ['page']
#store the session start time
session_start_time = session['time']
print
print session_start_time
#store the username
session_username = session['username']
print
print session_username
#find the next tracking event in time associated with the username
session_end = collection['tracking'].find_one({'username':session_username,'time':{ "$gt": session_start_time }})
print
print session_end
#store session end time
session_end_time = session_end['time']
print
print session_end_time
#calculate session watch duration
session_watch_duration =  datetime.strptime(session_end_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f") -  datetime.strptime(session_start_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
print
print session_watch_duration

#convert the session watch duration to seconds
session_watch_duration = session_watch_duration.total_seconds()
print
print session_watch_duration

if session_watch_duration <= 5:
    result.append([session_username, video_page, session_watch_duration])
else:
    result.append('less than 5 seconds')
print result

#session_end_type = session_end['event_type']




'''
result = []

output = CSV(result,['Username',], output_file='video_watch_duration.csv', row_limit=200000) 
output.generate_csv()
'''
