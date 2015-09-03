'''
InsertedX csv entrance and exit surveys into mongodb

***USAGE***

./survey_csv_to_mongod.py DB COLL SURVEY1 SURVEY2 ...

'''

import csv, json, collections, pymongo, os, sys

# SPECIFY database address
DATABASE_ADDRESS = "mongodb://localhost"

if len(sys.argv) < 4:
  print "Arguments missing..."
  print "Usage: ./survey_csv_to_mongod.py DB COLL SURVEY1 SURVEY2 ..."
  print "Exiting..."

DATABASE_NAME = sys.argv[1]
DATABASE_COLLECTION = sys.argv[2]
FILE_LIST = []

# build FILE_LIST
for arg in sys.argv[3:]:
  if os.path.isfile(arg): # if file
    FILE_LIST.append(arg)
  elif os.path.isdir(arg): # if directory
    rootdir = arg
    for root, subFolders, files in os.walk(rootdir):
      for file in files:
        FILE_LIST.append(os.path.join(root,file))

# filter for CSV files

# establish connection to the database
connection = pymongo.Connection(DATABASE_ADDRESS)
db = connection[DATABASE_NAME]
collection = db[DATABASE_COLLECTION]

error_count = 0

for csv_file in FILE_LIST:
  # file hander
  csv_read = open(csv_file,'rb')

  # check if the file is a valid csv
  try:
    # Perform various checks on the dialect (e.g., lineseparator,
    # delimiter) to make sure it's sane
    dialect = csv.Sniffer().sniff(csv_read.read(1024))
    # Reset the read position back to the start of the file before reading any entries.
    csv_read.seek(0)
  except csv.Error:
    # File appears not to be in CSV format
    print csv_file + " is not a valid CSV file"
    continue

  # file reader
  csv_read = csv.reader(csv_read)

  # skip header
  next(csv_read, None)

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
