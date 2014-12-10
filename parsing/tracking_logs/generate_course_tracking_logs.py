'''
This module will extract tracking logs for a given course and date range 
between when course enrollment start and when the course ended. For each log,
the parent_data and meta_data from the course_structure collection will be 
appended to the log based on the event key in the log


'''

import pymongo
import sys
from datetime import datetime
import json


def connect_to_db_collection(db_name, collection_name):
    '''
    Return collection of a given database name and collection name
    
    '''
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    collection = db[collection_name]
    return collection 

def load_config(config_file):
    '''
    Return course ids and ranges of dates from which course specific tracking
    logs will be extracted

    '''
    pass


def extract_tracking_logs(course_ids, start_date, end_date):
    '''
    Return all trackings logs that contain given ids and that contain dates
    within the given range

    '''
    pass

def main():
    if len(sys.argv) !=  2:
        usage_message = """usage: python course_db_name course_config_file 
            Provide name of course database to insert tracking logs to and 
            config file to load configurations
            """
            sys.stderr.write(usage_message % sys.argv[0])
            sys.exit(1)

    tracking = connect_to_db_collection('tracking_logs', 'tracking') 

if __name__ == '__main__':
    main()

