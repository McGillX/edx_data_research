# Load tracking logs to MongoDB

There are two main steps to load tracking logs provided by edX to MongoDB:

1. Load all tracking logs provided by edX to a master collection, tracking, in a database, tracking_logs
2. Extract course specific tracking logs from the tracking_logs database filtered by course ids of the course
  and the range of dates between date of course enrollment and date of course completion

### Setup

### Run

### Usage

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
