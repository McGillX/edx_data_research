#

### Outline of all the fields of every event type
```
Navigational Event Types: seq_goto - seq_next - seq_prev
event.old
event.new
event.id



```

mongoexport  --host localhost --db edx --collection logs_by_user --csv --out data.csv --fields username,time,session,page,ip,context,agent,event_source,event.id


,event_type,event.old,event.new,event.id