'''
This modules gathers the session time for each user everytime they logged in i.e. how long
did they stay logged in

Usage:

python session_info.py

'''
import csv
from datetime import datetime

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('tracking_atoc185x')
collection = connection.get_access_to_collection()

query = collection['tracking_atoc185x'].find()
users_to_sessions = {}
fail = []
for index, item in enumerate(query):
    try:
        if 'session' in item:
            if item["username"] in users_to_sessions:
                if item["session"] in users_to_sessions[item["username"]]:
                   users_to_sessions[item["username"]][item['session']].append(item["time"])
                else:
                   users_to_sessions[item["username"]][item['session']] = [item["time"]]
            else:
                users_to_sessions[item["username"]]  = {}
                users_to_sessions[item["username"]][item['session']] = [item["time"]]
    except:
        print "Fail -> %s" %item
        fail.append(item)

print "Number of fail: " + str(len(fail))
if fail:
    import json
    with open('report.txt', 'w') as outfile:
        json.dump(fail, outfile)
else:
    print "no fail"
result = []
for item in users_to_sessions:
    for nested_item in users_to_sessions[item]:
        max_time = max(users_to_sessions[item][nested_item])
        end_time = datetime.strptime(max_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
        min_time = min(users_to_sessions[item][nested_item])
        start_time = datetime.strptime(min_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
        result.append([item, nested_item, len(users_to_sessions[item][nested_item]), start_time, end_time, end_time - start_time])
output = CSV(result, ['Username', 'Session ID', 'Number of Events', 'Start Time', 'End Time', 'Time Spent'], output_file='session_info.csv')
output.generate_csv()
