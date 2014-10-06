'''
This module extract all the information filled by students for the entrance 
and exit survey

First step is to get ids of each page in the surveys. One may have to do this 
manually by:

1) Go to http://studio.edx.org and select the required course. For e.g., for
the course ATOC185x, go to https://studio.edx.org/course/McGillX/ATOC185x/2T2014

2) In the course outline, go to Entrance Survey and select the first page of the
entrance survey, e.g. General Info

3) On the new page that opens, click on 'View Live Version', this opens a page 
in a new tab

4) Click on 'STAFF DEBUG INFO'. Note that there are two links to 'STAFF 
DEBUG INFO', one at the top and one at the bottom. Select the one on the
bottom of the page

5) A small window should pop up. In the window, the value stored under location
is the id the of page General Info for the Entrance Survey e.g.
location = i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41

6) Once you get the id for one page of a survey, repeat above process to get 
ids of all the pages of both the Entrance and Exit Surveys

7) The ids will be used in the scripts below to extract all the information 
filled by students in the Entrance and Exit Surveys from the collection 
courseware_studentmodule of a given course.

Usage (after getting the ids of all the pages in the Entrance and Exit surveys): 

python entrance_exit_surveys.py 

'''

from collections import defaultdict
import json

# These modules can be found under reporting scripts. You will have to add them
# in the same directory as this script
from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('courseware_studentmodule', 'auth_user')
collection = connection.get_access_to_collection()

# Modify key-value pairs in survey_pages to the name of the survey pages and to 
# the problem ids that maps to the survey pages E.g. if a course have a 
survey_pages = {'entrance_survey' : {'general_info' : 'i4x://McGillX/ATOC185x/problem/e60f566b9a9342ac9b8dd3f92296af41', 
'demographics_background' : 'i4x://McGillX/ATOC185x/problem/8781ed8818064bf08722ee3175c2f356' , 
'aspirations_motivation' : 'i4x://McGillX/ATOC185x/problem/ca3486d4d1ef49ea8c6aa38534bab855'}, 
'exit_survey' : {'part_1' : 'i4x://McGillX/ATOC185x/problem/7620c0262e3d44049d73ba5fed62edfd',
'part_2': 'i4x://McGillX/ATOC185x/problem/c993861c76e5484d8233e702af2e4b3d'}}

survey_ids = [_id for page in survey_pages.values() for _id in page.values()]
cursor_courseware_studentmodule = collection['courseware_studentmodule'].find()
cursor_student = collection['auth_user']

# For each student, get the values filled in a survey page and store the results
# in a dictionary where the key is the username. The username is extracted from
# the auth_user collection using the student id stored in the courseware_studentmodule collection
result = defaultdict(list)
not_in_auth_user = set()
for document in cursor_courseware_studentmodule:
    if document['module_id'] in survey_ids:
        try:
            username = cursor_student.find_one({'id' : document['student_id']})['username']
            doc_json = json.loads(document['state'])
            if 'student_answers' in doc_json:
                result[username].append(doc_json['student_answers'])
        except:
            not_in_auth_user.add(document['student_id'])

# For loop to retrieve the names of all the survey pages. Since a student may
# not have filled all pages, we look for the longest list and use the values
# to retrieve the survey pages
for value in result.values():
    if len(value) == 5:
        survey_question_ids = {key for item in value for key in item.keys()}
        print survey_question_ids
        break

survey_question_ids = sorted(list(survey_question_ids))
csv_data = []
for username, survey_info in result.iteritems():
    temp = [''] * len(survey_question_ids) 
    for item in survey_info:
        for key,value in item.iteritems():
            index = survey_question_ids.index(key)
            if key in survey_question_ids:
                temp[index] = value
    temp.insert(0, username)
    csv_data.append(temp)

output = CSV(csv_data, ['Username'] +  survey_question_ids, output_file='entrance_exit_surveys.csv')
output.generate_csv()
