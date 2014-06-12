# mongo_forum_to_mongod.py

Loads the .mongo dicussion forum data into MongoDB

### Setup

```python
# SPECIFY input .mongo filepath
FILENAME = 'data/McGillX-CHEM181x-1T2014-prod.mongo'

# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_FORUM_COLLECTION = "forum"
```

### Run

```
python mongo_forum_to_mongod.py
```

# mongo_forum_to_csv.py

Deprecated. Working but more stable to use mongo shell terminal command. See [mongod_forum_to_csv.md](https://github.com/McGillX/mongo-conversion/blob/master/forum_parsing/mongod_forum_to_csv.md)

### Setup

```python
# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_FORUM_COLLECTION = "forum"

# SPECIFY output filename
OUTPUT_FILENAME = DATABASE_NAME + "_" + DATABASE_FORUM_COLLECTION + ".csv"

# SPECIFY key fields to read
KEYS = {"author_username":1,
              "_type":1,
              "_id":0}
```

### Run

```
python mongo_forum_to_csv.py
```

# mongo_forum_to_json.py

Converts a .mongo file directly to .json where all separated objects of the .mongo file are concatenated into one JSON object

### Setup

```python
# SPECIFY input .mongo filename
mongo_filename = 'McGillX-CHEM181x-1T2014-prod.mongo'

# SPECIFY output .json filename
json_filename = mongo_filename.replace('.mongo','.json')
```

### Run

```
python mongo_forum_to_json.py
```