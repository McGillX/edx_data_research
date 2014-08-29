'''
This module gets all the unique users who watched each video
'''
from pymongo import MongoClient
from pprint import pprint
import csv
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = 'edx'
#DATABASE_TRACKING_COLLECTION = 'seek_video'
DATABASE_TRACKING_COLLECTION = 'tracking'

client = MongoClient(DATABASE_ADDRESS)
db = client[DATABASE_NAME]
tracking = db[DATABASE_TRACKING_COLLECTION]
#query = {'$or' : [{'event_type' : 'problem_show'} ,{ '$and' : [{'event_type' : 'problem_check'}, {'event_source' : 'server'} ] } ]}

cursor = tracking.find({'event_type' : 'play_video'}).distinct("username")

with open('video_watchers_distinct_names.csv' , 'wb') as  csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Username'])
        for item in cursor:
	    print item
	    writer.writerow([item])


