'''
Load tracking logs to mongodb. Since tracking logs will be generated daily, we
will load all logs to a master tracking_logs database in a master collection
In this way, there will only one main collection of all tracking logs and this
will be used to extract course specific tracking logs to the coure specific 
tracking log collection in the course specific database

Tracking logs will have an extention of either .log or .log.gz

'''

import pymongo
import json
import glob
import sys
import gzip
import datetime
import os

ERRORFILE_SUFFIX = "-errors"

def connect_to_db_collection(db, collection):
    pass

def get_course_id(event):
    pass

def canonical_name(filepath):
    pass

def migrate_tracking_logs_to_mongo():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
