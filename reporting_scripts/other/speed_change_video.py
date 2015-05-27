'''
This module gets all the events per user while watching videos. 
Since we will need to sort a very large number of documents, you should create a separate collection to 
aggregate all required documents in one collection and then extract results from the new collection.

Command to run on the mongo shell to create new collection:

db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "speed_change_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "speed_change_video_data"}], {allowDiskUse : true})

Usage: 
python speed_change_video.py

'''

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV 

connection = EdXConnection('speed_change_video_data')
collection = connection.get_access_to_collection()
cursor = collection['speed_change_video_data'].find()
result = [[item['username'], item['parent_data']['chapter_display_name'], item['parent_data']['sequential_display_name'], item['parent_data']['vertical_display_name'], item['event']['old_speed'], item['event']['new_speed']] for item in cursor] 
output = CSV(result,['Username', 'Chapter Name','Sequential Name', 'Vertical Name', 'Old Speed', 'New Speed'], output_file='speed_change.csv') 
output.generate_csv()
