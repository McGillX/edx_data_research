'''
This module gets all the events per user while watching videos. Since we will
need to sort a very large number of documents, user should create a separate
collection to aggregate all required documents in one collection and then 
extract results from the new collection
Command to run on the mongo shell to creare new collection:

db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "seek_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "seek_video"}, {allowDiskUse : true}])

'''

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('seek_video')
collection = connection.get_access_to_collection()
sort_parameters = [('parent_data.chapter_display_name',1), ('parent_data.sequential_display_name',1), ('parent_data.vertical_display_name',1)]
cursor = collection['seek_video'].find()
result = []
for index, item in enumerate(cursor):
    if 'old_time' in item['event']:
        old_time = item['event']['old_time']
    else:
        old_time = 0
    result.append([item['username'], item['parent_data']['chapter_display_name'], item['parent_data']['sequential_display_name'], item['parent_data']['vertical_display_name'], old_time, item['event']['new_time']])

output = CSV(result,['Username', 'Chapter Name','Sequential Name', 'Vertical Name', 'Old Time', 'New Time'], output_file='seek_video.csv', row_limit=200000) 
output.generate_csv()
