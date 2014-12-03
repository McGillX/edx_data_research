'''
This script loads tracking logs to mongodb
Tracking logs are generated daily
we will load all logs to a master tracking_logs collection within our master database
From the master tracking logs collection we extract course specific tracking logs
Course specific tracking logs are loaded to a course specific database in collection called tracking

Note, this script works with both decompressed (.log) and compressed (.log.gz) tracking logs

'''

import pymongo
import json
import glob
import sys
import gzip
import datetime
import os

ERROR_FILE_SUFFIX = "-errors"

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
                for name in file_names:
                    logs.append(os.path.join(dir_path, name))
    return logs
    
def migrate_tracking_logs_to_mongo(tracking, tracking_imported):
    pass

def main():
    if len(sys.argv) < 4:
        usage_message = """usage: %s db coll f1 [f2] [f3...]
            For one or more files containing edx tracking logs, insert into the
            collection given. Files ending .gz they are decompressed on the fly
            Files successfully loaded are tracked in tracking_imported. If 
            already loaded, skip.
            """
        sys.stderr.write(usage_message % sys.argv[0])
        sys.exit(1)
        
    tracking, tracking_imported = connect_to_db_collection(sys.argv[1], sys.argv[2])
    log_files = get_tracking_logs(sys.argv[3:]) 
    for log in sorted(log_files):
        log_file_name = canonical_name(log)
        if tracking_imported.find({'_id' : log_file_name}) or log_file_name.endswith(ERROR_FILE_SUFFIX): 
            print "Log file {0} already loaded".format(log)
            continue
        print "Loading log file {0}".format(log)
        if log.endswith('.gz'):
            file_handler = gzip.open(log)
            log_content = file_handler.readlines()
            file_handler.close()
            event_source = log_file_name[:-3]
            error_file_name = event_source + ERROR_FILE_SUFFIX
        else:
            with open(log) as file_handler:
                log_content = file_handler.readlines()
            event_source = log_file_name
            error_file_name = event_source + ERROR_FILE_SUFFIX

if __name__ == '__main__':
    main()
