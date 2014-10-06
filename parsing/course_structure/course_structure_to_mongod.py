'''
Insert the edx course_structure-prod-analytics .json file into mongodb database for aggregation, see README.md

The one JSON object will be split into sub objects, in which all the first level keys will become the _id of its object value

'''

import pymongo
import json
import copy

# SPECIFY .mongo filepath
filename = 'data/McGillX-CHEM181x-1T2014-course_structure-prod-analytics.json'

# If user wants to pass path to file via command line arguments. then user can do the following:
# filename = sys.argv[1] # On the command line, user can run the command: python course_structure_to_mongod.py path_to_file


# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "course_structure"

# establish a connection to the database
connection = pymongo.Connection(DATABASE_ADDRESS)

# choose database
db = connection[DATABASE_NAME]

# choose collection
collection = db[DATABASE_COLLECTION]

# open the json file
json_file=open(filename)

# load the json data
json_data = json.load(json_file)

# find the categories (optional)
categories = []
for key in json_data:
  if json_data[key]['category'] and json_data[key]['category'] not in categories:
    categories.append(json_data[key]['category'])
print categories

# parse the key names
new_json_data = {}
for key in json_data:
  new_key = key.split('/')[-1]
  json_data[key]['_id'] = new_key
  if json_data[key]['children']:
    for index, child in enumerate(json_data[key]['children']):
      json_data[key]['children'][index] = child.split('/')[-1]
  new_json_data[new_key] = json_data[key]
json_data = new_json_data

# delete conditional
keys_to_delete = []
for key in json_data:
  if json_data[key]['category'] == 'conditional':
    # FIND PARENT_ID
    parent_id = None
    for key1 in json_data:
      if json_data[key1]['children'] and key in json_data[key1]['children']:
        parent_id = key1
    # PUT CHILD'S CHILDREN INTO PARENT'S CHILDREN LIST
    index_child = json_data[parent_id]['children'].index(key)
    left_list = json_data[parent_id]['children'][:index_child]
    right_list = json_data[parent_id]['children'][index_child+1:]
    json_data[parent_id]['children'] = left_list + json_data[key]['children'] + right_list
    keys_to_delete.append(key)

for key in keys_to_delete:
  del json_data[key]

# delete wrappers
keys_to_delete = []
for key in json_data:
  if json_data[key]['category'] == 'wrapper':
    # FIND PARENT_ID
    parent_id = None
    for key1 in json_data:
      if json_data[key1]['children'] and key in json_data[key1]['children']:
        parent_id = key1
    # PUT CHILD'S CHILDREN INTO PARENT'S CHILDREN LIST
    index_child = json_data[parent_id]['children'].index(key)
    left_list = json_data[parent_id]['children'][:index_child]
    right_list = json_data[parent_id]['children'][index_child+1:]
    json_data[parent_id]['children'] = left_list + json_data[key]['children'] + right_list
    keys_to_delete.append(key)
for key in keys_to_delete:
  del json_data[key]


# build the parent_data
error_count = 0
for key in json_data:
  # if the object has children
  if json_data[key]['children']:
    for index, child_key in enumerate(json_data[key]['children']):
      try:
        json_data[child_key]['parent_data'] = {}
      except:
        error_count += 1
        continue
      parent_category = json_data[key]['category']
      parent_order_key = parent_category + '_order'
      parent_id_key = parent_category + '_id'
      parent_display_name_key = parent_category + '_display_name'
      json_data[child_key]['parent_data'][parent_order_key] = index
      json_data[child_key]['parent_data'][parent_id_key] = json_data[key]['_id']
      json_data[child_key]['parent_data'][parent_display_name_key] = json_data[key]['metadata']['display_name']
print str(error_count) + ' errors'

# recursively combine parent_data from ancestor

# sequential
for key in json_data:
  if json_data[key]['category'] == 'sequential':
    chapter_id = json_data[key]['parent_data']['chapter_id']
    chapter_parent_data = json_data[chapter_id]['parent_data']
    json_data[key]['parent_data'].update(chapter_parent_data)
# vertical
for key in json_data:
  if json_data[key]['category'] == 'vertical':
    sequential_id = json_data[key]['parent_data']['sequential_id']
    sequential_parent_data = json_data[sequential_id]['parent_data']
    json_data[key]['parent_data'].update(sequential_parent_data)
# rest
for key in json_data:
  if json_data[key]['category'] != 'vertical' and json_data[key]['category'] != 'sequential' and json_data[key]['category'] != 'chapter' and json_data[key]['category'] != 'course':
    try:
      vertical_id = json_data[key]['parent_data']['vertical_id']
      vertical_parent_data = json_data[vertical_id]['parent_data']
      json_data[key]['parent_data'].update(vertical_parent_data)
    except:
      print json_data[key]

for key in json_data:
  collection.insert(json_data[key])
