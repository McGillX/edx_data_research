#!/usr/bin/env python -u

'''
Credits to jm from HarvardX, edx.org
Added some stuff to link to course_structure by michaelchum

DO NOT EXECUTE THIS DIRECTLY USE WITH load_log_mongod.sh
    
Load tracking logs into mongo using pymongo driver.  Correctly
handles the "event" fields (unjson-ifying it) and creates the course_id
    Created on Nov 8, 2012
    @author: jm, edx.org

usage: ./load_log_mongo.py DB COLL f1 f2

Supports multiple file names, globbed file names, and gzipped files.
'''

import pymongo
import json
import glob
import sys
import gzip
import datetime
import os

# SPECIFY log files path, specify the parent folder
indir = os.path.dirname(os.path.dirname(__file__))

ERRORFILE_SUFFIX = "-errors"

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

# MAIN

if len(sys.argv) < 4:
    usage_message = """usage: %s db coll f1 [f2] [f3...]

For one or more files containing edx tracking logs, insert into the
collection given. Files ending .gz they are decompressed on the fly.
Files successfully loaded are tracked in coll_incremental. If already
loaded, skip.
"""
    sys.stderr.write(usage_message % sys.argv[0])
    sys.exit(1)

db_name = sys.argv[1]
collection_name = sys.argv[2]

# Get database connection and collections
connection = pymongo.Connection('localhost', 27017)
db = connection[db_name]
events_coll = db[collection_name]
imported_coll = db[collection_name+"_imported"]

total_error = 0
total_success = 0

# Connect to course_structure database
STRUCTURE_COLLECTION_NAME = 'course_structure'
struct_coll = db[STRUCTURE_COLLECTION_NAME]

# Append course_structure info to record dict
def append_course_struct(id):
    try:
        data = struct_coll.find({"_id":id})[0]
        if 'parent_data' in data.keys():
            record['parent_data'] = data['parent_data']
        if 'metadata' in data.keys():
            record['metadata'] = data['metadata']
    except:
        #print "Structure not found for", id
        pass

# collect all files from command line
files = []
for i in sys.argv[3::]:     # all remaining arguments are lists of files to process
    for j in glob.glob(i):
        files.append(j)

skipped = 0;
first_skipped = None
last_skipped = None
for logfile_path in sorted(files):
    print logfile_path
    # if this file has already been imported, or an error file, skip
    logfile_path_canonical = canonical_name(logfile_path)
    if imported_coll.find({'_id':logfile_path_canonical}).count() or \
            logfile_path_canonical.endswith(ERRORFILE_SUFFIX):
        if not first_skipped:
            first_skipped = logfile_path_canonical
        last_skipped = logfile_path_canonical
        skipped += 1
        continue

    if skipped > 0:
        print "skipped %d files, %s ... %s" % (skipped, first_skipped, last_skipped)
        skipped = 0
        first_skipped = None
        last_skipped = None
    print "loading", logfile_path

    if logfile_path[-3:].lower() == ".gz":
        logfile = gzip.open(logfile_path)
        event_source = logfile_path[0:-3]
        errorfile = open(logfile_path[0:-3] + ERRORFILE_SUFFIX, "w")
    else:
        logfile = open(logfile_path)
        event_source = logfile_path
        errorfile = open(logfile_path + ERRORFILE_SUFFIX, "w")

    try:
        events_coll.remove({"load_file":logfile_path_canonical})
    except Exception as e:
        print "cannot remove prior records (%s), %s" % (logfile_path_canonical, e)
        pass

    imp = {}
    imp['_id'] = logfile_path_canonical
    imp['date'] = datetime.datetime.utcnow()
    imp['error'] = 0
    imp['good'] = 0
    imp['courses'] = {}
    for record_raw in logfile:
        try:
            record = json.loads(record_raw)
        except ValueError:
            imp['error'] += 1
            sys.stdout.write("p")
            errorfile.write("PARSE: " + record_raw)
            continue

        # Hack: the record when it is encoded as a string.  It's OK if
        # parsing fails, then just stick with existing string.
        if 'event' in record and not isinstance(record['event'], dict):
            try:
                event_dict = json.loads(record['event'])
                record['event'] = event_dict
            except ValueError:
                pass
        course_id = get_course_id(record)
        if course_id:
            record['course_id'] = course_id
            if course_id not in imp['courses']:
                imp['courses'][course_id] = 1
            else:
                imp['courses'][course_id] += 1
        record['load_date'] = datetime.datetime.utcnow()
        record['load_file'] = canonical_name(event_source)

        '''Bind parent_data and metadata from course_structure to every tracking document'''
        bound = False
        # Parse IDs and bind parent_data/
        if record['event']:
            if type(record['event']) is dict:
                if 'id' in record['event'].keys():
                    splitted = record['event']['id'].split('-')
                    if len(splitted) > 3:
                        record['event']['id'] = splitted[-1]
                        if not bound:
                            append_course_struct(record['event']['id'])
                            bound = True
                    splitted = record['event']['id'].split('/')
                    if len(splitted) > 3:
                        record['event']['id'] = splitted[-1]
                        if not bound:
                            append_course_struct(record['event']['id'])
                            bound = True
        if record['page']:
            splitted = record['page'].split('/')
            if len(splitted) > 2:
                record['page'] = splitted[-2]
                if not bound:
                    append_course_struct(record['page'])
                    bound = True
        '''End of binding'''
        try:
            res = events_coll.insert(record)
        except pymongo.errors.InvalidDocument as e:
            errorfile.write("INVALID_DOC: " + record_raw)
            sys.stdout.write("i")
            imp['error'] += 1
            continue
        except Exception as e:
            errorfile.write("ERROR: " + record_raw)
            sys.stdout.write("x")
            imp['error'] += 1
            continue

        imp['good'] += 1
        if (imp['error'] + imp['good']) % 10000 == 0:
            sys.stdout.write(".")
        if (imp['error'] + imp['good']) % 500000 == 0:
            sys.stdout.write("\n")

    # If we've inserted anything from this file, track in "inserted" coll
    if imp['good'] > 0:
        try:
            result = imported_coll.update({'_id': imp['_id']}, imp, 
                    upsert=True, safe=True)
        except pymongo.errors.DuplicateKeyError:
            print ("File already imported: %s", fname)

    total_error += imp['error']
    total_success += imp['good']
    sys.stdout.write("\n")

print "Total events read:  ", (total_error + total_success)
print "Inserted events:    ", total_success
print "Not loaded:         ", total_error
