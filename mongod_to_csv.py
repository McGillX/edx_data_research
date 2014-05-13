'''
Generic script to convert a Mongodb collection to CSV
Works for non-uniform collections
'''

import pymongo
import json
import csv
import copy

# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "logs_by_user"

CSV_FILENAME = DATABASE_NAME + "_" + DATABASE_COLLECTION + ".csv"

# CSV_FILENAME = 'single_use.csv'

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

def dict_keys_to_array(mydict):
  myarray = []
  for key in mydict.keys():
    myarray.append(key)
    if type(mydict[key]) is dict and len(mydict[key])>1:
      myarray.extend(dict_keys_to_array(mydict[key]))
  return myarray

def dict_values_to_array(mydict):
  myarray = []
  for key in mydict.keys():
    myarray.append(mydict[key])
    if type(mydict[key]) is dict and len(mydict[key])>1:
      myarray.extend(dict_values_to_array(mydict[key]))
  return myarray

def check_dict(mydict):
  for key in mydict.keys():
    try:
      mydict[key] = json.loads(mydict[key])
    except:
      continue
    if type(mydict[key]) is dict:
      mydict[key] = check_dict(mydict[key])
  return mydict

# def unicode_list_to_ascii(mylist):
#   for s in mylist:
#     if type(s) is unicode:
#       s.encode('utf-8','ignore')
#   return mylist

# def numerate_dict(mydict):
#   count = 0
#   for key in mydict.keys():
#     mydict[key]['index'] = count
#     count += 1
#     if type(mydict[key]) is dict and len(mydict[key]) > 1:
#       for sub_key in mydict[key].keys():
#         if sub_key!='index':
#           mydict[key][sub_key]['index'] = count
#           count += 1

def match_dict_to_generic_dict(mydict,gen_dict):
  for key in mydict.keys():
    try:
      if type(mydict[key]) is dict and len(mydict[key])!=1:
        gen_dict[key] = match_dict_to_generic_dict(mydict[key], gen_dict[key])
      else:
        gen_dict[key] = mydict[key]
    except:
      gen_dict[key] = mydict[key]
  return gen_dict

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
header_array = dict_keys_to_array(schema)

# write the title line
csv_writer.writerow(header_array)

# initialize cursor to entire collection
cursor = collection.find({'username':'Vicky_M','event_type':'problem_check'})

count_error = 0

# write the rest
for obj in cursor:
  gen_obj = match_dict_to_generic_dict(obj,copy.deepcopy(schema))
  arr_obj = dict_values_to_array(copy.deepcopy(gen_obj))
  # arr_obj = unicode_list_to_ascii(arr_obj)
  try:
    csv_writer.writerow(arr_obj)
  except:
    count_error += 1
    continue

print count_error

csv_file.close()
    # elif:
    #   try:
    #     fake_dict = json.loads(mydict[key])
    #     myarray.extend(dict_keys_to_array(fake_dict))
    #   except:
    #     continue





