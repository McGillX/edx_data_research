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
---

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

# mongod_to_csv
---

### Export the .mongo discussion database from a hosted mongo database to .csv for analysis

There are two different types of document structures in a .mongo file. They differ by _type ``Comment`` or ``Comment_Thread``

See the official edX docs on .mongo format:
https://github.com/edx/edx-platform/blob/master/docs/en_us/data/source/internal_data_formats/discussion_data.rst

This command exports a .csv file with all fields of both types of document.

Run this on a UNIX SHELL not the mongo shell

```
mongoexport --host localhost --db edx --collection forum --csv --out data.csv --fields _id.oid,_type,abuse_flaggers,anonymous,anonymous_to_peers,at_position_list,author_id,author_username,title,body,comment_thread_id.oid,course_id,created_at.date,endorsed,historical_abuse_flaggers,parent_ids,sk,update_at.date,visible,votes.count,votes.up,votes.down,votes.up_count,votes.down_count,votes.point,comment_count,at_position_list,commentable_id,closed,last_activity_at.date
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
