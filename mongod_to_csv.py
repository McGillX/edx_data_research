'''
Generic script to convert a Mongodb collection to CSV
Works for non-uniform collections
'''

import pymongo
import json
import csv

# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "logs_by_user"

CSV_FILENAME = DATABASE_NAME + "_" + DATABASE_COLLECTION + ".csv"

# establish a connection to the database
connection = pymongo.Connection(DATABASE_ADDRESS, safe=True)

# choose database
db = connection[DATABASE_NAME]

# choose collection
collection = db[DATABASE_COLLECTION]

# initialize cursor to entire collection
cursor = collection.find({"event_type":"seq_goto"}).limit(50)

schema = {}
# build the full schema in case the collection is non-uniform
for obj in cursor:
  print obj
  for key in obj.keys():
    if key == 'event':
      print obj['event']
  # for key in obj.keys():
  #   if key not in schema:
  #     schema[key] = []
  #   if type(obj[key]) is dict:
  #     for sub_key in obj[key]:
  #       if sub_key not in schema[key]:
  #         schema[key].append(sub_key)
