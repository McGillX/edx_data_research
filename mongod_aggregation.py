import pymongo
from bson.son import SON

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the edx database
db=connection.edx

# specify collection
forum = db.forum

# Output in JSON
obj = forum.aggregate([{"$group": {"_id": {"Username":"$author_username","Type":"$_type"}, "count": {"$sum": 1}}}])