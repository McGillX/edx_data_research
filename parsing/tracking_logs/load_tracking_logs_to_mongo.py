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
    db_name = db
    collection_name = collection
    
    # Get database connection and collections
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    tracking_collection = db[collection_name]
    imported_collection = db[collection_name + "_imported"]
    return tracking_collection, imported_collection

def get_course_id(event):
    """
    Try to harvest course_id from various parts of an event.  Assumes that
    the "event" has already been parsed into a structure, not a json string.
    The course_id should be of the format A/B/C and cannot contain dots.
    """
    course_id = None
    if event['event_source'] == 'server':
        # get course_id from event type
        if event['event_type'] == '/accounts/login/':
            s = event['event']['GET']['next'][0]
        else:
            s = event['event_type']
    else:
        s = event['page']
    if s:
        a = s.split('/')
        if 'courses' in a:
            i = a.index('courses')
            if (len(a) >= i+4):
                course_id = "/".join(a[i+1:i+4]).encode('utf-8').replace('.','')
    return course_id

def canonical_name(filepath):
    """
    Save only the filename and the subdirectory it is in, strip off all prior 
    paths.  If the file ends in .gz, remove that too.  Convert to lower case.
    """
    fname = '/'.join(filepath.lower().split('/')[-2:])
    if len(fname) > 3 and fname[-3:] == ".gz":
        fname = fname[:-3]
    return fname

def migrate_tracking_logs_to_mongo():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
