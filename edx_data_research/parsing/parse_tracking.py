'''
Loads tracking logs to mongodb

Tracking logs are generated daily. We will load all logs to a master
tracking_logs collection within our master database. From the master
tracking logs collection we extract course specific tracking logs.
Course specific tracking logs are loaded to a course specific database in
collection called tracking

Note, this script works with both decompressed (.log) and compressed (.log.gz) tracking logs

Note: use tracking as both the database_name and the collection_name

*Some errors occur when loading open assessments events
'''

import datetime
import gzip
import json
import os
import pymongo
import sys

from collections import defaultdict

from edx_data_research.parsing.parse import Parse

ERROR_FILE_SUFFIX = "-errors"

class Tracking(Parse):

    def __init__(self, args):
        super(Tracking, self).__init__(args)
        self.collections = ['tracking', 'tracking_imported']
        self.logs = args.logs

    def migrate(self):
        total_success = 0
        total_errors = 0
        log_files = self._get_tracking_logs(self.logs)
        for log in sorted(log_files):
            if not log.endswith(ERROR_FILE_SUFFIX):
                log_file_name = self._log_file_name(log)
                if self.collections['tracking_imported'].find_one({'_id': log_file_name}):
                    print 'Log file {0} already loaded'.format(log)
                    continue
                print 'Loading log file {0}'.format(log) 
                log_content = self._load_log_content(log)
                error_file_name = log + ERROR_FILE_SUFFIX
                errors, error_count, success_count = self._migrate_tracking_logs(
                                                     self.collections['tracking'],
                                                     self.collections['tracking_imported'],
                                                     log_content, log_file_name)
                total_success += success_count
                total_errors += error_count
                with open(error_file_name, 'w') as file_handler:
                    for error in errors:
                        file_handler.write('{0}\n'.format(error))
        print 'Total events read: {0}'.format((total_success + total_errors))
        print 'Inserted events: {0}'.format(total_success)
        print 'Not loaded: {0}'.format(total_errors)

    def _get_tracking_logs(self, path_to_logs):
        """
        Retrieve all logs files from command line whether they were passed directly
        as files or directory
        """
        logs = []
        for path in path_to_logs:
            if os.path.isfile(path):
                logs.append(path)
            elif os.path.isdir(path):
                for (dir_path, dir_names, file_names) in os.walk(path):
                    for name in file_names:
                        logs.append(os.path.join(dir_path, name))
        return logs

    def _log_file_name(self, file_path):
        """
        Save only the filename and the subdirectory it is in, strip off all prior
        paths.  If the file ends in .gz, remove that too.  Convert to lower case.
        """
        file_name = '/'.join(file_path.lower().split('/')[-1:])
        if len(file_name) > 3 and file_name[-3:] == ".gz":
            file_name = file_name[:-3]
        return file_name

    def _load_log_content(self, log):
        """Return log content"""
        if log.endswith('.gz'):
            file_handler = gzip.open(log)
            log_content = file_handler.readlines()
            file_handler.close()
        else:
            with open(log) as file_handler:
                log_content = file_handler.readlines()
        return log_content

    def _course_id(self, event):
        """
        Try to harvest course_id from various parts of an event.  Assumes that
        the "event" has already been parsed into a structure, not a json string.
        The course_id should be of the format A/B/C and cannot contain dots.
        """
        course_id = None
        if event['event_source'] == 'server':
            if event['event_type'] == '/accounts/login':
                s = event['event']['GET']['next'][0]
            else:
                s = event['event_type']
        else:
            s = event['event_type']
        if s:
            a = s.split('/')
            if 'courses' in a:
                i = a.index('courses')
                if len(a) >= (i + 4):
                    course_id = "/".join(a[i+1:i+4]).encode('utf-8').replace('.','')
        return course_id

    def _migrate_tracking_logs(self, tracking, tracking_imported, log_content,
                               log_file_name):
        """Migrate tracking logs to the tracking collection in the database"""
        errors = []
        log_to_be_imported = {'_id': log_file_name,
                              'date': datetime.datetime.utcnow(),
                              'error': 0, 'success': 0,
                              'courses': defaultdict(int)}
        for record in log_content:
            try:
                data = json.loads(record)
            except ValueError:
                log_to_be_imported['error'] += 1
                error.append('JSON LOAD: {0}'.format(record))
            
            try:
                log_to_be_imported['courses'][data['context']['course_id']] += 1
                data['course_id'] = data['context']['course_id']
            except KeyError:
                course_id = self._course_id(data)
                if course_id:
                    log_to_be_imported['courses'][course_id] += 1
                    data['course_id'] = course_id
            data['load_date'] = datetime.datetime.utcnow()
            data['load_file'] = log_file_name

            try:
                self.collections['tracking'].insert(data)
            except pymongo.errors.InvalidDocument as e:
                errors.append("INVALID_DOC ({0}): {1}".format(e, str(data)))
                log_to_be_imported['error'] += 1
                continue
            except Exception as e:
                errors.append("ERROR ({0}): {1}".format(e, str(data)))
                log_to_be_imported['error'] += 1
                continue
            log_to_be_imported['success'] += 1

        try:
            self.collections['tracking_imported'].insert(log_to_be_imported, check_keys=False)
        except Exception as e:
            errors.append("Error inserting into tracking_imported {0}: {1}".
                          format(e, str(log_to_be_imported)))

        return errors, log_to_be_imported['error'], log_to_be_imported['success']
