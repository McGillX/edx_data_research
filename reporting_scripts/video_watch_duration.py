'''
-start by aggregating a new collection:
db.tracking.aggregate([{ $limit : 30 },{$match:{$and:[{'event_source':'browser'},{$or:[{'event_type':'play_video'},{'event_type':'speed_change_video'},{'event_type':'seq_goto'}, {'event_type':'seq_next'}, {'event_type':'seq_prev'}, {'event_type':'page_close'}, {'event_type':'play_video'},{'event_type':'pause_video'}, {'event_type':'seek_video'}, {'event_type':'pause_video'}]}]}}, {$project:{"username":1, "event_type":1, 'time':1,"event":1}},{ $sort: {'username':1,'time':1}},{$out: "new_test_collection"}])

-get all the distinct usernames

-get every tracking event associated with a username and sort them oldest to newest -chronologically

-loop through the events for the user
--if it finds a play_video event that becomes the watch session start
--next event becomes the watch session end 

later version to consider all the pause, skip possibilities
    
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
