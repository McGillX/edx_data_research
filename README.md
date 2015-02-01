Data Analytics Platform
======

This is a public repository for the tools developed and used by the McGillX research team to package, analyse, and manipulate the data that is collected through McGill's online courses offered via the edX platform. 

##Contents

|Directory | Description
|:------:|----------
|parsing | Contains the scripts and procedures used to load the raw data (json, sql, csv, mongodb) from edx to MongoDB
|reporting_scripts | Contains scripts that were used for extracting and aggregating data for analysis 



Process Overview
------
1. edX Data Download and Decryption
2. Populating Mongo Databases
 1. Import of SQL, Mongo and JSON files
 2. Creation of Master Database for Tracking Logs
 2. Extraction of Course Specific for Tracking Logs
3. Extraction of csv datasets

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

1. For information on importing the Course structure JSON files see [parsing/course_structure](parsing/course_structure)
2. For information on importing the Mongo files [(Discussion Forum Data)](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/discussion_data.html) see [parsing/forum](parsing/forum)
3. For information on importing SQL files [(Student Info and Progress Data)](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/sql_schema.html) see [parsing/sql](parsing/sql)




####ii. Master Database for Tracking Logs

All tracking logs are stored in the Master database. From this data set, course specifc tracking logs are extracted and stored in a course specific database. 

tracking log data provided by edX is logged on a daily basis and are not course specific.

Master Database structure
Database name: tracking_logs
 Collection: tracking

Migrate tracking logs to Master Database with the script parsing/tracking_logs/load_tracking_logs_to_mongo.py

####iii. Course Specific Collection for Tracking Logs

Course specific tracking log data is filtered by course ID as well as course enrollment start date and course end date.

Note: Before extracting the tracking logs of a course make sure the course structure data has been migrated to the course specific database. A subset of the course structure data is appended to the corresponding record in the tracking log. 
Ensure the course_structure data for the given course has been migrated to its own collection in the course database. The data is provided in json format and can be migrated using the script parsing/course_structure/course_structure_to_mongod.py

Generate course specific tracking log collections

1. Setup config file for given course by following the template template_config.json. This config file will be used to extract course specific tracking logs between the specific course start of enrollment date and end of course date
2. Run script generate_course_tracking_logs.py under parsing/tracking_logs to create a new collection that will contain tracking logs of given course along with some data from the course_structure collection

3. Extraction of csv datasets
----
*documentation in progress*

4. Anonymize csv datasets
----
*documentation in progress*

## Contact

You can contact McGillX for any help in running the scripts, setting up or just an explanation about a specific script:

McGillX - <mcgillx.tls@mcgill.ca>

## Contribute

If you would like to add new scripts, improve existing scripts, or found an error in the script feel free to send a pull request or raise an issue.





