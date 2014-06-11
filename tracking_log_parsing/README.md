# Load multiple tracking logs to MongoDB

Load the edX tracking logs to MongoDB, targets a folder (recursively)

### Setup

MongoDB instance has to be local

```bash
DATABASE="edx"
COLLECTION="tracking"
DIRECTORY="CHEM181x_logs_decrypted"
```

### Run

Might require sudo

```
sh LOAD.sh
```

# load_log_mongo.py

### Usage

```
python load_log_mongo.py DB COLL f1 f2
```

# mongod_log_to_csv.py

Export the tracking logs from MongoDB to csv. 

WARNING: Only attempt on a small collection of tracking logs (less than 1 million documents). DO NOT run on the entire course. 

### Setup

```python
# SPECIFY connection details
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "logs_by_user"

# SPECIFY output csv file
CSV_FILENAME = DATABASE_NAME + "_" + DATABASE_COLLECTION + ".csv"
```

### Run

```
python mongod_log_to_csv.py
```