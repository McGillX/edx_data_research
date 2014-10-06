## Overview
The scripts in this folder either extract survey information filled by the user from mongoDB to a csv file or viceversa depending on whether you want the survey data in a csv file or imported to a MongoDB collection

### 1. survey_csv_to_mongod.py 

Load the edx entrance and exit surveys to MongoDB

#### Setup

```python
# SPECIFY csv input filepath
CSV_FILENAME = "data/ExitPage2.csv"

# SPECIFY database info to insert/create
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "exit_survey"
```

#### Run

```
python survey_csv_to_mongod.py
```

### 2. survey_csv_to_csv.py

Parse the survey .csv into a more readable .csv by filtering all the JSON brackets and separating the fields into columns

#### Setup

```python
# SPECIFY csv input filepath
CSV_FILENAME = "data/ExitPage2.csv"

# SPECIFY csv output file
CSV_OUTPUT_FILENAME = CSV_FILENAME.replace(".csv","_PARSED.csv")
```

#### Run

```
python survey_csv_to_csv.py
```
### 3. Extract Entrance and Exit Surveys from tracking logs in MongoDB to a csv file
In this script, all you have to do is replace the values in the object survey_pages (line 49) with the problem_id of a survey page. 

	    survey_pages = {'entrance_survey' : {'general_info' : 'i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41', 'demographics_background' : 'i4x://McGillX/ATOC185x/problem/8781ed8818064bf08722ee3175c2f356' , 'aspirations_motivation' : 'i4x://McGillX/ATOC185x/problem/ca3486d4d1ef49ea8c6aa38534bab855'}, 'exit_survey' : {'part_1' : 'i4x://McGillX/ATOC185x/problem/7620c0262e3d44049d73ba5fed62edfd','part_2': 'i4x://McGillX/ATOC185x/problem/c993861c76e5484d8233e702af2e4b3d'}}
	    
Once you have updated the values of the survey pages with the correct problem_ids, run the following command to extract the surveys