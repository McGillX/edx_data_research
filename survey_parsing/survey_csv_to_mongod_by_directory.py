'''
InsertedX csv entrance and exit surveys into mongodb

'''

import csv, json, collections, pymongo, os, sys

# SPECIFY database info to insert/create
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "exit_survey"

# DEFAULT directory path
DATA_DIRECTORY = "data"

file_list = []

# Check for argument
rootdir = sys.argv[1]
for root, subFolders, files in os.walk(rootdir):
    for file in files:
        fileList.append(os.path.join(root,file))
print "Files found in folder:"
print file_list

# establish connection to the database
connection = pymongo.Connection(DATABASE_ADDRESS)
db = connection[DATABASE_NAME]
collection = db[DATABASE_COLLECTION]

error_count = 0

for csv_file in file_list:
  # file hander
  csv_read = open(csv_file,'rb')

  # check if the file is a valid csv
  try:
    # Perform various checks on the dialect (e.g., lineseparator,
    # delimiter) to make sure it's sane
    dialect = csv.Sniffer().sniff(csv_fileh.read(1024))
    # Reset the read position back to the start of the file before reading any entries.
    csv_fileh.seek(0)
  except csv.Error:
    # File appears not to be in CSV format
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