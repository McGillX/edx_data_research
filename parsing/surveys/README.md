# survey_csv_to_mongod.py 

Load the edx entrance and exit surveys to MongoDB

### Setup

```python
# SPECIFY csv input filepath
CSV_FILENAME = "data/ExitPage2.csv"

# SPECIFY database info to insert/create
DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = "edx"
DATABASE_COLLECTION = "exit_survey"
```

### Run

```
python survey_csv_to_mongod.py
```

# survey_csv_to_csv.py

Parse the survey .csv into a more readable .csv by filtering all the JSON brackets and separating the fields into columns

### Setup

```python
# SPECIFY csv input filepath
CSV_FILENAME = "data/ExitPage2.csv"

# SPECIFY csv output file
CSV_OUTPUT_FILENAME = CSV_FILENAME.replace(".csv","_PARSED.csv")
```

### Run

```
python survey_csv_to_csv.py
```

