Data Analytics Platform
======

This is a public repository for the tools developed and used by the McGillX research team to package, analyse, and manipulate the data that is collected through McGill's online courses offered via the edX platform. 

Contents
--------

|Directory | Description
|:------:|----------
|parsing | Contains the scripts and procedures used to load the raw data (json, sql, csv, mongodb) from edx to MongoDB
|reporting_scripts | Contains scripts that were used for extracting and aggregating data for analysis 



Overview
------
Before starting the setup consult with edX to setup keys and credentials for data transfer


<ol>
    <li><a href="#1-edx-data-download-and-decryption">edX Data Download and Decryption</a></li>
    <li> <a href="#2-populating-mongo-databases">Populating Mongo Databases</a></li>
    <ol>
        <li>Import of SQL, Mongo and JSON files</li>
        <li>Creation of Master Database for Tracking Logs</li>
        <li>Extraction of Course Specific for Tracking Logs</li>
    </ol>
    <li> <a href="#3-extract-csv-datasets">Extract csv datasets</a></li>
    <li><a href="#4-anonymize-csv-datasets">Anonymize csv datasets</a></li>
</ol>
<p>
<img src="https://docs.google.com/drawings/d/17GHG0-01iaHpshhi9WYktv4g2dIc4unWwmibZ5QHofI/pub?w=1308&h=603"/>
</p>

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
McGillX uses [Python 2.7](https://www.python.org/download/releases/2.7/) scripts to populate and analyze a [Mongo Database](https://www.mongodb.org/). In order to execute the following setup you will need to have python 2.7, mongodb and [PyMongo](https://api.mongodb.org/python/current/) installed on your machine. Note some scripts require the installation of specific python libraries in order to run.

####McGillX Database Outline

*documentation in progress*

####Course Specific Database Structure
* Each McGillX course has one database with the following collections to store each dataset delivered by edx:

All data packages except the tracking logs are course specific as provided by edx 

| Raw Data Packages | Collection Name* |
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

*Please use the collection names outlined above to avoid import and report generation issues.

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
   python course_structure_to_mongod.py <database_name> course_structure* <path_to_json_file>
   ```
    *Be sure the name the course structure collection "course_structure" using the command above
2. Parse the [Discussion Forum Data](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/discussion_data.html) - [parsing/forum](parsing/forum)
 1. Run mongod
 2. Run [mongo_forum_to_mongod.py](parsing/forum/mongo_forum_to_mongod.py)
 
   ```
   python mongo_forum_to_mongod.py <database_name> <path_to_forum_mongo_file>
   ```

3. Parse the [Student Info and Progress Data](http://edx.readthedocs.org/projects/devdata/en/latest/internal_data_formats/sql_schema.html) - [parsing/sql](parsing/sql)
 1. Run mongod
 2. Run to following commands from the console:

`mongoimport -d <database_name> -c <collection_name*> --type tsv --file <path_to_file>`

*Use the collection names outlined below to avoid issues

Enter the appropriate SQL file names
   ```
   mongoimport -d <database_name> -c auth_userprofile --type tsv --file {org}-{course}-{date}-auth_userprofile-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c certificates_generatedcertificate --type tsv --file {org}-{course}-{date}-certificates_generatedcertificate-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c student_courseenrollment --type tsv --file {org}-{course}-{date}-student_courseenrollment-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c auth_user --type tsv --file {org}-{course}-{date}-auth_user-prod-analytics.sql --headerline

   mongoimport -d <database_name> -c courseware_studentmodule --type tsv --file {org}-{course}-{date}-courseware_studentmodule-prod-analytics.sql --headerline
   
   mongoimport -d <database_name> -c courseware_studentmodule --type tsv --file {org}-{course}-{date}-user_id_map-prod-analytics.sql --headerline
   
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

   A second collection called {collection_name}_imported is automatically generated to keep track of what files were successfully imported and errors that occured
   
   **_Errors:_** {org}-edx-events-{date}.log.gz-errors files are generated when documents are not successfully loaded to the database
  - Some events associated with openassessments generate errors. We are working to resolve the issue.
 
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
   ```
{
    
    "edx_id" : "",
    "edx_course_name" : "",
    "course_ids" : ["", ""],
    "date_of_course_enrollment" : "YYYY-MM-DD",
    "date_of_course_completion" : "YYYY-MM-DD"

}
   ```
 - A single course may have multiple course ID's associated with its events. Search the main tracking collection for potential course ID's. From the mongo shell execute the following for a print out of the course ID's:
   `db.tracking.distinct('course_id')`
2. Run [generate_course_tracking_logs.py](/parsing/tracking_logs/generate_course_tracking_logs.py) 
   ```
python generate_course_tracking_logs.py <source_db> <source_collection> <destination_db> <destination_collection> <path_to_config_file>
   ```



3. Extract csv datasets - [report_scripts](/reporting_scripts) 
----
*documentation in progress*

<ul>
    <li><a href="#demographics">Demographics</a></li>
    <li><a href="#page-interaction">Page Interaction</a></li>
    <li><a href="#forum">Forum</a></li>
    <li><a href="#access-and-performance">Access and Performance</a></li>
    <li><a href="#navigation">Navigation</a></li>
</ul>

<h4 id="demographics">Demographics</h4>

<table style="undefined;table-layout: fixed; width: 445px">
<colgroup>
<col style="width: 190px">
<col style="width: 255px">
</colgroup>
  <tr>
    <th>Script</th>
    <th>Description / csv fields / Notes</th>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/ip_to_country.py">ip_to_country.py</a></td>
    <td>
        <ul>
            <li>Maps IP address of user tracking events to the associated country</li>
            <li>Username, IP</li>
            <li>There may be multiple ip addresses per user and some IP addresses may lack an associated username. When a user is not logged in the server emits an anonymous event that has not associated username.</li>
        </ul>
      </td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/user_info.py">user_info.py</a></td>
    <td>
        <ul>
            <li>Retrieve info about students registered in the course</li>
            <li>User ID,'Username', 'Final Grade', 'Gender', 'Year of Birth', 'Level of Education', 'Country', 'City'</li>
            <li>This script accesses the collections: 'certificates_generatedcertificate', 'auth_userprofile'</li>
        </ul>
    </td>
  </tr>
</table>

<h4 id="page-interaction">Page Interaction</h4>

<table style="undefined;table-layout: fixed; width: 445px">
<colgroup>
<col style="width: 190px">
<col style="width: 255px">
</colgroup>
  <tr>
    <th>Script</th>
    <th>Description / csv fields / Notes</th>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/show_transcript_completers.py">show_transcript_completers.py</a></td>
    <td>Retrieve the completers (users who completed the course) and filters all those who had event_type 'show_transcript'</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/session_info.py">session_info.py</a></td>
    <td>Gather the session time for each user everytime they logged in i.e. how long did they stay logged in</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/speed_change_video.py">speed_change_video.py</a></td>
    <td>Gets all the events per user when they changed speed of videos</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/seek_video.py">seek_video.py</a></td>
    <td>Gets all the events per user while watching videos</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/sequential_aggregation.py">sequential_aggregation.py</a></td>
    <td>Gather the number of various categories under each sequential including the number of html, videos, verticals etc.</td>
  </tr>
</table>

<h4 id="forum">Forum</h4>

<table style="undefined;table-layout: fixed; width: 445px">
<colgroup>
<col style="width: 190px">
<col style="width: 255px">
</colgroup>
  <tr>
    <th>Script</th>
    <th>Description / csv fields / Notes</th>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/forum_stats.py">forum_stats.py</a></td>
    <td>Calculates the number of forum threads and posts for a given course</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/forum_data.py">forum_data.py</a></td>
    <td>Get data for each comment thread and comment in the forum</td>
  </tr>
            <tr>
                <td><a href="/reporting_scripts/forum_body_extraction_for_word_cloud.py">forum_body_extraction_for_word_cloud.py</a></td>
    <td>Extract all of the comments and comment threads from the forum of a given course using NLTK</td>
  </tr>
</table>
        
<h4 id="access-and-performance">Access and Performance</h4>
            
<table style="undefined;table-layout: fixed; width: 445px">
<colgroup>
<col style="width: 190px">
<col style="width: 255px">
</colgroup>
  <tr>
    <th>Script</th>
    <th>Description / csv fields / Notes</th>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/date_of_registration_completers.py">date_of_registration_completers.py</a></td>
    <td>Get the date of registration of all users who completed the course</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/course_completers.py">course_completers.py</a></td>
    <td>Extract the usernames of the course completers</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/activities_with_lower_completion.py">activities_with_lower_completion.py</a></td>
    <td>Get the number of students who answered a given problem correctly or incorrectly</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/activity_count_completers.py">activity_count_completers.py</a></td>
    <td>Get the number of completers who did each activity</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/chapters_accessed_per_user.py">chapters_accessed_per_user.py</a></td>
    <td>Determines how many chapters were accessed by each user for a given course</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/failure_analysis.py">failure_analysis.py</a></td>
    <td>extracts all the videos watched and the problems attempted by users who got grades between 50% and 59% inclusive</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/first_activity_completers.py">first_activity_completers.py</a></td>
    <td>Retrieve the first activity of all user who completed a course</td>
  </tr>
</table>

<h4 id="navigation">Navigation</h4>

<table style="undefined;table-layout: fixed; width: 445px">
<colgroup>
<col style="width: 190px">
<col style="width: 255px">
</colgroup>
    <tr>
    <th>Script</th>
    <th>Description / csv fields / Notes</th>
  </tr>
  <tr>
    <td><a href="/reporting_scripts/navigation_tabs_data.py">navigation_tabs_data.py</a></td>
    <td>Get the number of users who access each navigation tab</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/navigation_tabs_data_date.py">navigation_tabs_data_date.py</a></td>
    <td>Get the number of times each Navigation tab was clicked/viewed for each day during the course</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/navigation_tabs_data_date_completers.py">navigation_tabs_data_date_completers.py</a></td>
    <td>Get the number of times each Navigation tab was clicked/viewed, by students who completed the course, for each day during the course</td>
  </tr>
  <tr>
      <td><a href="/reporting_scripts/navigational_events_completers.py">navigational_events_completers.py</a></td>
    <td>Count the number of navigation events: seq_next, seq_prev, seq_goto for those students who completed the course</td>
  </tr>
</table>


4. Anonymize csv datasets
----
*documentation in progress*

|Script | Description
|:------:|----------
|[username_to_hash_id_reports.py](/reporting_scripts/username_to_hash_id_reports.py)| Take a csv report as input and maps usernames to their hash ids and user ids and return a new csv_report

## Contact

You can contact McGillX for any help in running the scripts, setting up or just an explanation about a specific script:

McGillX - <mcgillx.tls@mcgill.ca>

## Contribute

If you would like to add new scripts, improve existing scripts, or found an error in the script feel free to send a pull request or raise an issue.





