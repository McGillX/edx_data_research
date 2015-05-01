'''

1) Create a new collection in the mongo shell:

db.tracking_collection.aggregate([{$match :{$or : [{"event_type" : "seek_video"}, {"event_type" : "play_video"},{"event_type":"pause_video"}]}}, {$out : "video_watch_duration_collection"}])

2) Run: python video_watch_duration.py


desired final output.csv

username, video, chapter, vertical, sequential, watch duration

get the event_types : play_video, pause_video, seek_video

watch duration should include ONLY:

- time between play_video -> another video event (pause_video or seek_video)
- time between seek_video : {'new_time' : Time}  -> pause video (only with new_time > old_time, this is to avoid including rewinds)
- 



play_video(when user presses play on video console, may not be 0) -> pause video time
watch periods:
    event_type : pause_video - "event_type":"play_video" {"event":{"currentTime":TIME}} = add to watch duration
    if seek_video : {'old_time' : TIME} > seek_video : {'new_time' : TIME} = rewind (exclude from watch duration)
    if seek_video : {'old_time' : TIME} < seek_video : {'new_time' : TIME} 
      "pause_video" {"event":{"currentTime":TIME}} - seek_video : {'new_time': TIME } = add to watch duration

'''

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('video_watch_duration_collection')
collection = connection.get_access_to_collection()
cursor = collection['video_watch_duration_collection'].find()

result = []

output = CSV(result,['Username',], output_file='video_watch_duration.csv', row_limit=200000) 
output.generate_csv()
