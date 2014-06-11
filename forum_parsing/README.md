# mongo_forum_to_mongod.py

### Setup

### Run

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
```

### Run

```
python mongo_forum_to_csv.py
```

# mongo_forum_to_json.py

### Setup

### Run