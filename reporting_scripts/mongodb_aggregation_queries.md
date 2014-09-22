# About
Mongo Aggregation Queries used on the mongo shell to output new collections with results of the aggregation queries

### Seek Video data
db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "seek_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "seek_video"}], {allowDiskUse : true})

### Speed change data
db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "speed_change_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "speed_change_video_data"}, {allowDiskUse : true}])
