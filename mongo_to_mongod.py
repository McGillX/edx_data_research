import pymongo
import sys
import traceback
import json

# 1. Start mongod
# 2. Start mongo shell
# 3. In mongo shell, create "edX" database by typing "use edx"
# 4. Run this script specifying the .mongo filename in edxmongo_to_mongodb() function 
# 5. Enjoy a clean database

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the edx database
db=connection.edx
forum = db.forum

# Filter the .json object to a format accepted by mongodb
def remove_dollar_sign(obj):
  # MongoDB does not accept '$' as key values
  # Loop through all the keys and filter out '$'
  for key in obj.keys():
    if type(obj[key]) is dict:
      for key1 in obj[key].keys():
        new_key1 = key1.replace('$','')
        if new_key1 != key1:
          obj[key][new_key1] = obj[key][key1]
          del obj[key][key1]
    # Some values inside the object are 'parent_ids':[{'$oid': u'52e0082cfbd06391ba0000a4'}]
    # The [{}] will trigger an error in MongoDB (not 100% sure)
    # Here, [] and '$' are filtered out
    if type(obj[key]) is list and len(obj[key])==1 and type(obj[key][0]) is dict:
      for key2 in obj[key][0].keys():
        new_key2 = key2.replace('$','')
        if new_key2!=key2:
          temp_value = obj[key][0][key2]
          del obj[key]
          obj[key] = { new_key2:temp_value }
  return obj

def edxmongo_to_mongodb():

  # specify file
  filename = 'McGillX-CHEM181x-1T2014-prod.mongo'

  # file handler
  mongo_file = open(filename,'r')

  try:
    for line in mongo_file:
      obj = json.loads(line)
      obj = remove_dollar_sign(obj)
      forum.insert(obj)

  except:
    # print "Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]
    for frame in traceback.extract_tb(sys.exc_info()[2]):
      fname,lineno,fn,text = frame
      print "Error in %s on line %d" % (fname, lineno)
      print sys.exc_info()[0],sys.exc_info()[1]

      #print line in document that causes error
      #print [...]

  mongo_file.close()

# function call
edxmongo_to_mongodb()
