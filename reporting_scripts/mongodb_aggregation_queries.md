# About
Mongo Aggregation Queries used on the mongo shell to output new collections with results of the aggregation queries

### 1 - Seek Video data
db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "seek_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "seek_video"}], {allowDiskUse : true})

### 2 - Speed change data
db.tracking_atoc185x.aggregate([{$match : {$and : [{"event_type" : "speed_change_video"},{ "parent_data": { $exists: true } }]}}, {$sort : {"parent_data.chapter_display_name" : 1, "parent_data.sequential_display_name" : 1, "parent_data.vertical_display_name" : 1}}, {$out : "speed_change_video_data"}, {allowDiskUse : true}])

### 3 - Number of video watchers per week
db.tracking_atoc185x.aggregate([{$group : { _id : { "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name","vertical_name" : "$parent_data.vertical_display_name"},students : {$addToSet:"$username"}}}, {$unwind : "$students"} ,{$group : {_id: "$_id", num_of_students : {$sum : 1}}}, {$out : "username_count_chapter_name"}])

### 4 - Number of attempts to get correct answer to a problem
db.tracking_atoc185x.aggregate([{$match : {'event_type': 'problem_check', 'event_source' : 'server', "event.success" : 'correct'}}, {$group : { _id :  {"username" : "$username", "problem_id" : "$event.problem_id" }, num_of_attempts : {$sum : 1}}}, {$out : 'count_of_correct_attemps'}]) 

### 5 - Number of incorrect attempts to a problem
db.tracking_atoc185x.aggregate([{$match : {'event_type': 'problem_check', 'event_source' : 'server', "event.success" : 'incorrect'}}, {$group : { _id :  {"username" : "$username", "problem_id" : "$event.problem_id" }, num_of_attempts : {$sum : 1}}}, {$out : 'count_of_incorrect_attemps'}])

### 6 - Number of attempts to a problem by getting the maximum number of attempts by a user on a problem_id
db.tracking_atoc185x.aggregate([{$match : {event_type : 'problem_check', event_source : 'server'}}, {$group : {_id : {"username" : "$username", "problem_id" : "$event.problem_id"}, max_num_of_attempts : {$max : '$event.attempts'}}}, {$out : "num_of_attempts"}])

### 7 - Average number of attempts for each problem id sorted in descending order (collection num_of_attempts was created from query 6 above)
db.num_of_attempts.aggregate([{$group : {_id : {"chapter_name" : "$_id.chapter_name","sequential_name" : "$_id.sequential_name", "vertical_name" : "$_id.vertical_name" ,"problem_id" : "$_id.problem_id"}, avg_num_of_attempts : {$avg : "$max_num_of_attempts"}}}, {$sort : {avg_num_of_attempts : -1}}, {$out : "avg_num_of_attempts"}])

### 8 - Count the number of unique users who answered a problem successfully
db.tracking_atoc185x.aggregate([{$match : {"event_type" : "problem_check", "event_source" : "server", "event.success": correct}}, {$group : { _id : { "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name","vertical_name" : "$parent_data.vertical_display_name", "problem_id" : "$event.problem_id"},students : {$addToSet:"$username"}}}, {$unwind : "$students"} ,{$group : {_id: "$_id", num_of_students : {$sum : 1}}}, {$out : {username_unique_count_success_correct}}])

