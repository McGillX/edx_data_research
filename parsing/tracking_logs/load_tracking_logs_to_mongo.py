'''
This script loads tracking logs to mongodb
Tracking logs are generated daily
we will load all logs to a master tracking_logs collection within our master database
From the master tracking logs collection we extract course specific tracking logs
Course specific tracking logs are loaded to a course specific database in collection called tracking

Note, this script works with both decompressed (.log) and compressed (.log.gz) tracking logs

'''

import pymongo
import sys
import json
import gzip
import datetime
import os
from collections import defaultdict

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
    
def load_log_content(log):
    '''
    Return log content 

    '''
    if log.endswith('.gz'):
        file_handler = gzip.open(log)
        log_content = file_handler.readlines()
        file_handler.close()
    else:
        with open(log) as file_handler:
            log_content = file_handler.readlines()
    return log_content

def migrate_tracking_logs_to_mongo(tracking, tracking_imported, log_content, log_file_name):
    '''
    Migrate tracking logs to the tracking collection in the database

    '''
    errors = []
    log_to_be_imported = {}
    log_to_be_imported['_id'] = log_file_name
    log_to_be_imported['date'] = datetime.datetime.utcnow()
    log_to_be_imported['error'] = 0
    log_to_be_imported['good'] = 0
    log_to_be_imported['courses'] = defaultdict(int)
    for record in log_content:
        try:
            data = json.loads(record)
        except ValueError:
            log_to_be_imported['error'] += 1
            errors.append("PARSE: " + record )

        if 'event' in data and not instance(data['event'], dict):
            try:
                event_dict = json.loads(record['event'])
                data['event'] = event_dict
            except ValueError:
                pass
        course_id = get_course_id(data)
        data['course_id'] = course_id
        log_to_be_imported['courses'][course_id] += 1
        data['load_date'] = datetime.datetime.utcnow()
        data['load_file'] = log_file_name
        try:
            tracking.insert(data)
        except pymongo.errors.InvalidDocument as e:
            errors.append("INVALID_DOC: " + data)
            log_to_be_imported['error'] += 1
            continue
        except Exception as e:
            errors.append("ERROR: " + data)
            log_to_be_imported['error'] += 1
            continue
        log_to_be_imported['good'] += 1
    try:
        tracking_imported.insert(log_to_be_imported)
    except Exception as e:
        errors.append("Error inserting into tracking_imported: " + log_to_be_imported)
    return errors, log_to_be_imported['error'], log_to_be_imported['good']
            

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
    total_success = 0
    total_errors = 0
    log_files = get_tracking_logs(sys.argv[3:]) 
    for log in sorted(log_files):
        if not log.endswith(ERROR_FILE_SUFFIX):
            log_file_name = canonical_name(log)
            if tracking_imported.find({'_id' : log_file_name}): 
                print "Log file {0} already loaded".format(log)
                continue
            print "Loading log file {0}".format(log)
            log_content = load_log_content(log)
            error_file_name = log_file_name + ERROR_FILE_SUFFIX
            errors, error_count, success_count  = migrate_tracking_logs_to_mongo(tracking, tracking_imported, log_content, log_file_name)
            total_success += success_count
            total_errors += error_count
            with open(error_file_name, 'w'):
                '\n'.join(errors)

    print "Total events read: ", (total_success + total_errors)
    print "Inserted events: ", total_success
    print "Not loaded: ", total_errors

if __name__ == '__main__':
    main()
