'''

1) Create a new collection in the mongo shell:

db.tracking_collection.aggregate([{$match :{$or : [{"event_type" : "seek_video"}, {"event_type" : "play_video"},{"event_type":"pause_video"}]}}, {$out : "video_watch_duration_collection"}])

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
'''

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('video_watch_duration_collection')
collection = connection.get_access_to_collection()
cursor = collection['video_watch_duration_collection'].find()

result = []

output = CSV(result,['Username',], output_file='video_watch_duration.csv', row_limit=200000) 
output.generate_csv()
