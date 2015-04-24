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
