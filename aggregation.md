# Useful commands for aggregation

Count number of tracking events per user

### Number of unique users in tracking logs
```
db.tracking.aggregate([{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"unregistration_user_count"}])
```

### 
db.tracking.aggregate([{$match:{"event_type":{$not:/edx\.course\.enrollment.*/}}},{$group:{"_id":"$username","event_count":{$sum:1}}},{$out:"number_did_something"}])


db.tracking.aggregate([{$match:{"event_type":/edx\.course\.enrollment.*/}},{$out:"unregistration_event"}])




