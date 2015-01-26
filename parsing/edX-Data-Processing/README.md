Data Analytics Platform
======

A modularized system for managing data collected through McGill's online courses offered via the edX platform. 

Process Overview
------
1. edX Data Download and Decryption
2. Populating Mongo Databases
3. Creation of Master Database for Tracking Logs
4. Extraction of Course Specific for Tracking Logs
5. Extraction of csv datasets

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

2. Populating Database
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
| Tracking Logs     | tracking |

There are two components to populating the course specific databases:
1. For the Mongo and SQL files listed above the files are directly imported into each course's database
2. The tracking logs are first imported into a Master Database and then extracted for course specific databases 

####Master Database for Tracking Logs

All tracking logs are stored in the Master database. From this data set, course specifc tracking logs are extracted and stored in a course specific database. 

tracking log data provided by edX is logged on a daily basis and are not course specific.

Master Database structure
Database name: tracking_logs
 Collection: tracking

Migrate tracking logs to Master Database with the script parsing/tracking_logs/load_tracking_logs_to_mongo.py

#####Course Specific Collection for Tracking Logs

Course specific tracking log data is filtered by course ID as well as course enrollment start date and course end date.

Note: Before extracting the tracking logs of a course make sure the course structure data has been migrated to the course specific database. A subset of the course structure data is appended to the corresponding record in the tracking log. 
Ensure the course_structure data for the given course has been migrated to its own collection in the course database. The data is provided in json format and can be migrated using the script parsing/course_structure/course_structure_to_mongod.py

Generate course specific tracking log collections

1. Setup config file for given course by following the template template_config.json. This config file will be used to extract course specific tracking logs between the specific course start of enrollment date and end of course date
2. Run script generate_course_tracking_logs.py under parsing/tracking_logs to create a new collection that will contain tracking logs of given course along with some data from the course_structure collection
