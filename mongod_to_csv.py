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
cursor = collection.find()

# entire schema of our database
schema = {}

# dictionary of event_type matching the keys in event
event_type_match_event = {}

dict_event_types = []
non_dict_event_types = []

def dict_to_array(mydict):
  myarray = []
  for key in mydict:
    myarray.append(key)
    if type(mydict[key]) is dict:
      myarray.extend(dict_to_array(mydict[key]))
  return myarray

# def number_dict(mydict,count):
#   for key in mydict.keys():
#     mydict[key]['index'] = count
#     count += 1
#     if len(mydict[key])>1:
#       mydict[key],count = number_dict(mydict[key],count)
#   return mydict,int(count)


# build the full schema in case the collection is non-uniform
for obj in cursor:
  # build the dictionaries
  if type(obj['event']) is dict:
    if obj['event_type'] not in dict_event_types: 
      dict_event_types.append(obj['event_type'])
      if not (len(obj['event'].keys())==2 and 'GET' in obj['event'].keys() and 'POST' in obj['event'].keys()):
        event_type_match_event[obj['event_type']] = list(obj['event'].keys())
  else:
    if obj['event_type'] not in non_dict_event_types: 
      non_dict_event_types.append(obj['event_type'])
  # build the schema
  for key in obj.keys():
    if key not in schema:
      schema[key] = {}
    if type(obj[key]) is dict:
      for sub_key in obj[key]:
        if sub_key not in schema[key]:
          schema[key][sub_key] = {}

# output file handler
csv_file = open(CSV_FILENAME,'w+')
csv_writer = csv.writer(csv_file)

# produce an array for the header
header_array = dict_to_array(schema)

header_dict = number_dict(schema,0)

# write the title line
csv_writer.writerow(header_array)

# initialize cursor to entire collection
cursor = collection.find()

# write the rest
for obj in cursor:
  for key in obj.keys():
    pass

csv_file.close()





