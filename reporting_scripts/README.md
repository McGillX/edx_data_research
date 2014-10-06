## Overview

The reporting_scripts folder contains scripts that were used for various data analysis tasks on data of students that took a McGill online course with the edX platform. The data was provided by edX in various formats: sql, mongo and json. All such data was migrated to a local MongoDB database using scripts under the edX-data-research folder. 

The reporting_scripts folder also contains a file, mongodb_aggregation_queries.md, which contains a list of aggregation queries used directly on the mongo shell. The output of the aggregation queries were usually directed to a new Mongo collection and later migrated to a csv file. 

## Getting Started

### Tracking Logs
The tracking logs provided by edX are structured such that the logs for each day are accumulated. This may result in the logs of various courses under the same source to be combined. 

For example, McGill offered two courses this year, CHEM181x and ATOC181x. And the tracking logs may contain logs on both courses. So it is advised to first create a new collection based on the original tracking logs collection, that only contains logs for a specific course. This is to ensure that results of any aggregation query or reporting script will only contains results for a given course. The following example shows steps to retrieve tracking logs of only the course ATOC185x:

Get all unique course_ids in the tracking logs collections. The following query can be used:
   
    db.tracking.distinct('context.course_id')
   
   The above query would give a result similar to:

    [ "McGillX/ATOC185x/2T2014",
	"McGillX/CHEM181x/1T2014",
	"McGillX/CHEM181x_2/3T2014" ]
   
Use the following aggregation query to retrieve only those documents from the tracking collection that have the course ids of the required course:

    db.tracking.aggregate([{$match :{ 'context.course_id' : 'McGillX/ATOC185x/2T2014' }}, {$out : 'tracking_atoc185x'}])   
   
### Running a script
The description of a script and its usage is documented at the top of each script. If you are having difficulty running a script, please do not hesitate to contact us for help.

### What is base_edx.py and generate_csv_report.py? 

Most of the scripts in the reporting scripts folder make use of the modules based_edx and generate_csv_report. The purpose of base_edx is to remove the need to repeat steps of creating a connection to the MongoDB databse and getting access to different collections. Since this part is repeated on all scripts, I decided to make it a separate module and all the user has to do when creating an object of base_edx is to provide the require collections for data analysis

generate_csv_report is to remove the steps of remembering  how to open a csv file and not forget to close a csv file. It also take cares of the case where if the csv file is too big, for example bigger than 2 million and hence cannot be opened as an Excel file, the module will take care of splitting the output into multiple csv files. The default value for the maximum number of rows of a csv file is chosen to be 100,000 but that can be modified in the constructor. An important point to note when using the generate_csv_report module is that it expects the data (that needs to be written in a csv file) to be in the form of a 2D array or a list of lists. 

## Contact

You can contact the following people for any help in running the scripts, setting up or just an explanation about a specific script:

* Usman Ehtesham Gul - uehtesham90@gmail.com
* Alexander Steeves-Fuentes - alexander.steeves-fuentes@mcgill.ca

## Contribute

If you want to add any new scripts, or improve existing scripts, or you found an error in the script feel free to send a pull request or raise an issue
