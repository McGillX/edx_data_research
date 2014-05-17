'''
InsertedX csv entrance and exit surveys into mongodb
'''

import csv, json, collections, pymongo

# SPECIFY csv input file
CSV_FILENAME = "ExitPage2.csv"

# SPECIFY database info to insert/create
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "exit_survey"

# establish connection to the database
connection = pymongo.Connection(DATABASE_ADDRESS, safe=True)
db = connection[DATABASE_NAME]
collection = db[DATABASE_COLLECTION]

# file hander
csv_read = csv.reader(open(CSV_FILENAME,'rb'))

# skip header
next(csv_read, None)

error_count = 0

for line in csv_read:
  try:
    state_dict = json.loads(line[1])
  except:
    error_count += 1
    continue
  state_dict['username'] = str(line[0])
  try:
    collection.insert(state_dict)
  except:
    print state_dict
    break

print str(error_count) + ' errors'