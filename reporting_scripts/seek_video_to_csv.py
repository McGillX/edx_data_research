from pymongo import MongoClient
from pprint import pprint
import csv
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = 'edx'
DATABASE_TRACKING_COLLECTION = 'seek_video'

client = MongoClient(DATABASE_ADDRESS)
db = client[DATABASE_NAME]
tracking = db[DATABASE_TRACKING_COLLECTION]
#tracking.ensure_index([('parent_data.chapter_display_name',1), ('parent_data.sequential_display_name',1), ('parent_data.vertical_display_name',1)])
#query = {'$or' : [{'event_type' : 'problem_show'} ,{ '$and' : [{'event_type' : 'problem_check'}, {'event_source' : 'server'} ] } ]}
sort_parameters = [('parent_data.chapter_display_name',1), ('parent_data.sequential_display_name',1), ('parent_data.vertical_display_name',1)]

cursor = tracking.find({}).sort(sort_parameters)
data_csv = csv.writer(open('seek_video.csv', 'w'))
data_csv.writerow(['Username', 'Chapter Name','Sequential Name', 'Vertical Name', 'Old Time', 'New Time'])
for index, item in enumerate(cursor):
    print index, item['_id']
    if 'old_time' in item['event']:
        old_time = item['event']['old_time']
    else:
	old_time = 0
    data_csv.writerow([item['username'], item['parent_data']['chapter_display_name'], item['parent_data']['sequential_display_name'], item['parent_data']['vertical_display_name'], old_time, item['event']['new_time']])
   # print data
   # break
print index
