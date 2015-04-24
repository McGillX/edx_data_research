Data Analytics Platform
======

This is a public repository for the tools developed and used by the McGillX research team to package, analyse, and manipulate the data that is collected through McGill's online courses offered via the edX platform. 

Contents
--------

|Directory | Description
|:------:|----------
|parsing | Contains the scripts and procedures used to load the raw data (json, sql, csv, mongodb) from edx to MongoDB
|reporting_scripts | Contains scripts that were used for extracting and aggregating data for analysis 



Process Overview
------
Before starting the setup consult with edX to setup keys and credentials for data transfer

1. [edX Data Download and Decryption](#1-edx-data-download-and-decryption)
2. [Populating Mongo Databases](#2-populating-mongo-databases)
 1. Import of SQL, Mongo and JSON files
 2. Creation of Master Database for Tracking Logs
 2. Extraction of Course Specific for Tracking Logs
3. [Extract csv datasets](#3-extract-csv-datasets)
4. [Anonymize csv datasets](#4-anonymize-csv-datasets)

1. edX Data Download and Decryption
------

We use the file transfer client Cyberduck to access the amazon s3 server

1. Click Open Connection
2. In the new window that opens:
 1. Select S3 (Amazon Simple Storage Service) from the dropdown
 2. Enter the Access Key ID and Secret Access Key which has been provided to you by edX
 3. Click connect
3. To access the tracking logs click "Go" from the top menu bar 

   Do not try finding the tracking logs in the default course directory

4. Select "Go to Folder"
5. In the new window that opens enter the file path /edx-course-data
6. Find the name of your institution in the directory

   A directory with the following file structure should display:
 
   \insituition  
   -\edge  
   --\events  
   ---\YEAR  
   ----\InstitutionName-ex-events-YYYY-MM-DD.log.gz.gpg  
   
   -\edx  
   --\events  
   ---\YEAR  
   ----\InstitutionName-ex-events-YYYY-MM-DD.log.gz.gpg  

   The trackings logs are contained in the encrypted .gpg files
   
7. Download your files of interest
8. Decrypt the files using [Kleopatra Gpg4win](http://gpg4win.org/) 

2. Populating Mongo Databases
----
McGillX uses MongoDB 

####Course Specific Database Structure
* Each McGillX course has one database with the following collections to store each dataset delivered by edx:

All data packages except the tracking logs are course specific as provided by edx 

| Raw Data Packages | Collection Name |
| --------------------------------------------------------   |:-------------:  | |
|{org}-{course}-{date}-auth_user-{site}-analytics.sql| user |
|{org}-{course}-{date}-auth_userprofile-{site}-analytics.sql| userprofile |
|{org}-{course}-{date}-certificates_generatedcertificate-{site}-analytics.sql| certificates |
|{org}-{course}-{date}-courseware_studentmodule-{site}-analytics.sql| courseware_studentmodule |
| {org}-email_opt_in-{site}-analytics.csv   | NOT IN USE |
| {org}-{course}-{date}-student_courseenrollment-{site}-analytics.sql    | enrollment |
| {org}-{course}-{date}-user_api_usercoursetag-{site}-analytics.sql | NOT IN USE |
| {org}-{course}-{date}-user_id_map-{site}-analytics.sql    | user_id_map |
| {org}-{course}-{date}-{site}.mongo     | forum |
| {org}-{course}-{date}-wiki_article-{site}-analytics.sql     | NOT IN USE |
| {org}-{course}-{date}-wiki_articlerevision-{site}-analytics.sql     | NOT IN USE |
| {org}-{course}-{date}-course_structure-{site}-analytics.json     | course_structure |
| Tracking Logs     | tracking |

*{site} always appears as "prod"*

There are two components to populating the course specific databases:

1. For the Mongo and SQL files listed above the files are directly imported into each course's database
2. The tracking logs are first imported into a Master Database and then extracted for course specific databases 

####i. Creation of Course Specific Database (excluding tracking logs)

JSON, Mongo and SQL files are directly imported into each course's database

1. Parse the Course Structure - [parsing/course_structure](parsing/course_structure)
 1. Run mongod
 2. Run [course_structure_to_mongod.py](parsing/course_structure/course_structure_to_mongod.py)
 
   ```
   python course_structure_to_mongod.py <database_name> <collection_name> <path_to_json_file>
   ```
 
2. Parse the [Discussion Forum Data](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/discussion_data.html) - [parsing/forum](parsing/forum)
 1. Run mongod
 2. Run [mongo_forum_to_mongod.py](parsing/forum/mongo_forum_to_mongod.py)
 
   ```
   python mongo_forum_to_mongod.py <database_name> <path_to_forum_mongo_file>
   ```

3. Parse the [Student Info and Progress Data](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/sql_schema.html) - [parsing/sql](parsing/sql)
 1. Run mongod
 2. Run to following commands from the console:

Enter the appropriate SQL file names
   ```
   mongoimport -d <database_name> -c auth_userprofile --type tsv --file {org}-{course}-{date}-auth_userprofile-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c certificates_generatedcertificate --type tsv --file {org}-{course}-{date}-certificates_generatedcertificate-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c student_courseenrollment --type tsv --file {org}-{course}-{date}-student_courseenrollment-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c auth_user --type tsv --file {org}-{course}-{date}-auth_user-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c courseware_studentmodule --type tsv --file {org}-{course}-{date}-courseware_studentmodule-prod-analytics.sql --headerline
   ```





####ii. Master Database for Tracking Logs

- Tracking log data provided by edX is logged on a daily basis. The log files are not course specific.
- All tracking logs are stored in the Master database.
- Course specifc tracking logs are extracted and stored in a course specific database. 

Master Database structure:

- Database name: tracking_logs
- Collection: tracking

Migrate tracking logs to Master Database - [parsing/tracking_logs](parsing/tracking_logs)
 1. Run mongod
 2. Run [load_tracking_logs_to_mongo.py](parsing/tracking_logs/load_tracking_logs_to_mongo.py)
 
   ```
   python load_tracking_logs_to_mongo.py <database_name> <collection_name> <path_to_directory_containing_trackings_logs>
   ```


 
####iii. Course Specific Collection for Tracking Logs

Course specific tracking log data is filtered by course ID as well as course enrollment start date and course end date.

This process creates a new collection that will contain tracking logs of given course along with extracts from the course_structure collection.

**_Note_**
- Before extracting the tracking logs of a course make sure the course structure data has been migrated to the course specific database. 
- A subset of the course structure data is appended to the corresponding record in the tracking log. 
Ensure the course_structure data for the given course has been migrated to its own collection in the course database. 
- The data is provided in json format and can be migrated using the script parsing/course_structure/course_structure_to_mongod.py

Generate course specific tracking log collections - [parsing/tracking_logs](parsing/tracking_logs) 

1. Setup [template_config.json](/parsing/tracking_logs/course_config/template_config.json)
 - Create a config file for each course using the template 
 - The config file will be used to extract course specific tracking logs between the specified course start of enrollment date and end of course date

2. Run [generate_course_tracking_logs.py](/parsing/tracking_logs/generate_course_tracking_logs.py) 
```
generate_course_tracking_logs.py 
```



3. Extract csv datasets
----
*documentation in progress*
*documentation in progress*

|Script | Description|csv fields | Notes|
| ---: | --- | --- | --- |
|ip_to_country.py | Map IP address of given event to country | 'Username, 'IP' | There may be multiple ip adresses per user and some IP addresses may lack an associated username|
|user_info.py | Retrieve info about students registered in the course | 'User ID','Username', 'Final Grade', 'Gender', 'Year of Birth', 'Level of Education', 'Country', 'City' | This script accesses the collections: 'certificates_generatedcertificate', 'auth_userprofile'|
|show_transcript_completers.py| Retrieve the completers (users who completed the course) and filters all those who had event_type 'show_transcript' |
|session_info.py| Gather the session time for each user everytime they logged in i.e. how long did they stay logged in
|speed_change_video.py| Gets all the events per user when they changed speed of videos
|seek_video.py|Gets all the events per user while watching videos
|sequential_aggregation.py| Gather the number of various categories under each sequential including the number of html, videos, verticals etc.
|forum_stats.py | Calculates the number of forum threads and posts for a given course
|forum_data.py| Get data for each comment thread and comment in the forum
|date_of_registration_completers.py| Get the date of registration of all users who completed the course
|course_completers.py| Extract the usernames of the course completers
|activities_with_lower_completion.py| Get the number of students who answered a given problem correctly or incorrectly
|activity_count_completers.py| Get the number of completers who did each activity
|chapters_accessed_per_user.py| Determines how many chapters were accessed by each user for a given course
|failure_analysis.py| extracts all the videos watched and the problems attempted by users who got grades between 50% and 59% inclusive
|first_activity_completers.py| Retrieve the first activity of all user who completed a course
|forum_body_extraction_for_word_cloud.py| Extract all of the comments and comment threads from the forum of a given course using NLTK
|navigation_tabs_data.py| Get the number of users who access each navigation tab
|navigation_tabs_data_date.py| Get the number of times each Navigation tab was clicked/viewed for each day during the course
|navigation_tabs_data_date_completers.py| Get the number of times each Navigation tab was clicked/viewed, by students who completed the course, for each day during the course
|navigational_events_completers.py| Count the number of navigation events: seq_next, seq_prev, seq_goto for those students who completed the course

4. Anonymize csv datasets
----
*documentation in progress*

|Script | Description
|:------:|----------
|username_to_hash_id_reports.py| Take a csv report as input and maps usernames to their hash ids and user ids and return a new csv_report

## Contact

You can contact McGillX for any help in running the scripts, setting up or just an explanation about a specific script:

McGillX - <mcgillx.tls@mcgill.ca>

## Contribute

If you would like to add new scripts, improve existing scripts, or found an error in the script feel free to send a pull request or raise an issue.





