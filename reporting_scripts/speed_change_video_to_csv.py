'''
This module gets the user info for speed changes while watching a video
'''
from pymongo import MongoClient
from pprint import pprint
import csv
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = 'edx'
#DATABASE_TRACKING_COLLECTION = 'seek_video'
DATABASE_TRACKING_COLLECTION = 'speed_change'

client = MongoClient(DATABASE_ADDRESS)
db = client[DATABASE_NAME]
tracking = db[DATABASE_TRACKING_COLLECTION]
sort_parameters = [('parent_data.chapter_display_name',1), ('parent_data.sequential_display_name',1), ('parent_data.vertical_display_name',1)]

cursor = tracking.find({}).sort(sort_parameters)
i = 0
data_csv = csv.writer(open('speed_change.csv', 'w'))
data_csv.writerow(['Username', 'Chapter Name','Sequential Name', 'Vertical Name', 'Old Speed', 'New Speed'])
for index, item in enumerate(cursor):
    data_csv.writerow([item['username'], item['parent_data']['chapter_display_name'], item['parent_data']['sequential_display_name'], item['parent_data']['vertical_display_name'], item['event']['old_speed'], item['event']['new_speed']])
