'''
This module will extract tracking logs for a given course and date range 
between when course enrollment start and when the course ended. For each log,
the parent_data and meta_data from the course_structure collection will be 
appended to the log based on the event key in the log


'''

import pymongo
import sys


def main():
    db_name = sys.argv[1]
    collection_name = sys.argv[2]
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    tracking = db[collection_name]

if __name__ == '__main__':
    main()

