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
    tracking = db[collection_name]
    tracking_imported = db[collection_name + "_imported"]
    return tracking, tracking_imported

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
    fname = '/'.join(filepath.lower().split('/')[-1:])
    if len(fname) > 3 and fname[-3:] == ".gz":
        fname = fname[:-3]
    return fname

def get_tracking_logs(path_to_logs):
    '''
    Retrieve all logs files from command line whether they were passed directly
    as files or directory

    '''

    logs = []
    for item in path_to_logs: 
        if os.path.isfile(item):
            logs.append(item)
        elif os.path.isdir(item):
            for (dir_path, dir_names, file_names) in os.walk(item):
                logs.extend(file_names)
    return logs
    
def migrate_tracking_logs_to_mongo(tracking, tracking_imported):
    pass

def main():
    if len(sys.argv) < 4:
        usage_message = """usage: %s db coll f1 [f2] [f3...]
            For one or more files containing edx tracking logs, insert into the
            collection given. Files ending .gz they are decompressed on the fly.
            Files successfully loaded are tracked in coll_incremental. If already
            loaded, skip.
            """
        sys.stderr.write(usage_message % sys.argv[0])
        sys.exit(1)
        
    tracking, tracking_imported = connect_to_db_collection(sys.argv[1], sys.arv[2])

if __name__ == '__main__':
    main()
