Load tracking logs to MongoDB
====

There are two main steps to load tracking logs provided by edX to MongoDB:

1. Load all tracking logs provided by edX to a master collection, tracking, in a database, tracking_logs
2. Extract course specific tracking logs from the tracking_logs database filtered by course ids of the course
  and the range of dates between date of course enrollment and date of course completion

## Load general tracking logs to tracking_logs database
### Setup
You need to provide path to directory which contain all the log files or path to the log files that need to be migrated to the database or a combination of both. You can pass multiple arguments

### Run
1. Pass path to directory to logs

        $ python load_tracking_logs_to_mongo.py db_name collection_name <path_to_directory>

2. Pass path to log files

        $ python load_tracking_logs_to_mongo.py db_name collection_name <path_to_file_1> <path_to_file_2> ...

3. Pass path to log files and directory

        $ python load_tracking_logs_to_mongo.py db_name collection_name <path_to_directory_1> <path_to_directory_2> <path_to_file_1> <path_to_file_2> ...

## Load course specific tracking logs to course database

### Setup
1) Ensure the course_structure collection has been generated for the course. If not, then some information will not be added to tracking logs

2) Create config file for desired course. Follow the format in template_config.json to create the course specific config file. For example for the the course CHEM181x, create file chem181x_config.json with the following configurations:

    {
    
    	"edx_id" : "chem181x",
    	"edx_course_name" : "Food for Thought",
    	"course_ids" : ["McGillX/CHEM181x/1T2014"],
       	"date_of_course_enrollment" : "2013-10-15",
    	"date_of_course_completion" : "2014-05-01"
    	
    }

### Run
    python generate_course_tracking_logs.py course_db_name <path_to_config_file>
mongod_log_to_csv.py
====

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
