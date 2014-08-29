'''
This modules gathers the session time for each user everytime they logged in i.e. how long
did they stay logged in

'''
from pymongo import MongoClient
from pprint import pprint
import csv
from datetime import datetime
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = 'edx'
DATABASE_TRACKING_COLLECTION = 'tracking'

client = MongoClient(DATABASE_ADDRESS)
db = client[DATABASE_NAME]
tracking = db[DATABASE_TRACKING_COLLECTION]
#query = tracking.find({"session" : "a30aa421a768a4c75c4ce0156a540e20"})
query = tracking.find()
#query = tracking.find({"username" : ""})
users_to_sessions = {}
fail = []
for index, item in enumerate(query):
    #print index
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

print "Number of fail: " + len(fail)
if fail:
    import json
    with open('report.txt', 'w') as outfile:
        json.dump(fail, outfile)
else:
    print "no fail"
with open("session_info.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Username', 'Session ID', 'Number of Events', 'Start Time', 'End Time', 'Time Spent'])
    for i in users_to_sessions:
    	#data = [i]
	for j in users_to_sessions[i]:
            #print j, len(users_to_sessions[i][j])
	    max_time = max(users_to_sessions[i][j])
            #print max_time
            end_time  = datetime.strptime(max_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
            min_time = min(users_to_sessions[i][j])
            #print min_time
            start_time = datetime.strptime(min_time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
            #print "Time difference: " + str(a - b)	
	    writer.writerow([i, j, len(users_to_sessions[i][j]), start_time, end_time, end_time - start_time])
