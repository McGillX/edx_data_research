Data Migration to MongoDB
================

All raw data provided by edx (json, csv, mongo) is loaded to MongoDB using scripts in this folder. 

##Contents

|Directory | Description
|:------:|----------
|course_structure | Load data for course structure to MongoDBMigrate data from discussion forum to MongoDB
|forum | Load data from discussion forum to MongoDB  
|sql| Load SQL files to MongoDB using MongoDB's mongoimport command
|tracking_logs| Load all the tracking logs to MongoDB
