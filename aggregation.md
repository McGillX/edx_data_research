# Useful commands for aggregation on MongoDB database

Count number of tracking events per user

### Number of unique users in tracking logs
db.tracking.aggregate([{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"unregistration_user_count"}])

### Number of unique users who did something else than registering/unregistering
#### number_did_something
db.tracking.aggregate([{$match:{"event_type":{$not:/edx\.course\.enrollment.*/}}},{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"number_did_something"}])

### Last event of every unique user
####last_event_by_user

db.tracking.aggregate([{ $sort: { "time": 1 } }, { $group: { "_id":"$username", "date":{ $last:"$time" }, "last_event_type": { $last:"$event_type" }, "metadata": { $last:"$metadata" }, "parent_data": { $last:"$parent_data" } } }, {$out:"last_event_by_user"} ])

# Mongo Shell

db.tracking.find().sort( { time: -1 } )

# Mongoexport to CSV

#### last_event_by_user.csv

mongoexport --host localhost --db edx --collection last_event_by_user --csv --out last_event_by_user.csv --fields _id,date,last_event_type,metadata.display_name,parent_data.course_display_name,parent_data.chapter_display_name,parent_date.sequential_display_name,parent_data.vertical_display_name




