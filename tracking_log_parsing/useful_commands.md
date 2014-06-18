# Useful commands for aggregation

Count number of tracking events per user

### Number of unique users in tracking logs
```
db.tracking.aggregate([{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"number_events_per_user"}])
```

### 
db.tracking.aggregate([{$match:{$not:{$or:[{"event_type":"edx.course.enrollment.deactivated"},{"event_type":"edx.course.enrollment.activated"}]}}},{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"number_did_something"}])


{"event_type":{$not:"edx.course.enrollment.deactivated"}} 