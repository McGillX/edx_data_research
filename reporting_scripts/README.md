## Overview

The reporting_scripts folder contains scripts that were used for various data analysis tasks on data of students that took a McGill online course with the edX platform. The data was provided by edX in various formats: sql, mongo and json. All such data was migrated to a local MongoDB database using scripts under the edX-data-research folder. 

The reporting_scripts folder also contains a file, mongodb_aggregation_queries.md, which contains a list of aggregation queries used directly on the mongo shell. The output of the aggregation queries were usually directed to a new Mongo collection and later migrated to a csv file. 

## Getting Started

### Tracking Logs
The tracking logs provided by edX are structured such that the logs for each day are accumulated. This may result in the logs of various courses under the same source to be combined. 

For example, McGill offered two courses this year, CHEM181x and ATOC181x. And the tracking logs may contain logs on both courses. So it is advised to first create a new collection based on the original tracking logs collection, that only contains logs for a specific course. This is to ensure that results of any aggregation query or reporting script will only contains results for a given course. The following example shows steps to retrieve tracking logs of only the course ATOC185x:

1. Get all unique course_ids in the tracking logs collections. The following query can be used:
   
   db.tracking.distinct('event.course_id')
   
   The above query would give a result similar to:

   [
	"McGillX/ATOC185x/2T2014",
	"McGillX/CHEM181x/1T2014",
	"McGillX/CHEM181x_2/3T2014"
   ]
   
2. Use the following aggregation query to retrieve only those documents from the tracking collection that have the course ids of the required course:

   db.tracking.aggregate([{$match :{ 'event.course_id' : '' }}, {$out : 'tracking_atoc185x'}])   
   
### Running a script
The description of a script and its usage is document at the top of each script. If you are having difficulty running a script or not able to run a script, please do not hesitate to contact us for help. 

## Contact

You can contact the following people for any help in running the scripts, setting up or just an explanation about a specific script:

* Usman Ehtesham Gul - uehtesham90@gmail.com
* Alexander Steeves-Fuentes - alexander.steeves-fuentes@mcgill.ca

## Contribute

If you want to add any new scripts, or improve existing scripts, or you found an error in the script feel free to send a pull request or raise an issue

