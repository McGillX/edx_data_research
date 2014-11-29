'''
Load tracking logs to mongodb. Since tracking logs will be generated daily, we
will load all logs to a master tracking_logs database in a master collection
In this way, there will only one main collection of all tracking logs and this
will be used to extract course specific tracking logs to the coure specific 
tracking log collection in the course specific database

Tracking logs will have an extention of either .log or .log.gz

'''
