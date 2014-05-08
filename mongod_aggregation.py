import pymongo
from bson.son import SON

# establish a connection to the database
connection = pymongo.Connection("mongodb://localhost", safe=True)

# get a handle to the edx database
db=connection.edx

# specify collection
forum = db.forum

print forum.aggregate([
            {"$group": {"_id": "$author_id", "count": {"$sum": 1}}}
          ])