'''
Insert the edx course_structure-prod-analytics .json file into mongodb database for aggregation, see README.md

The one JSON object will be split into sub objects, in which all the first level keys will become the _id of its object value

'''

import pymongo
import json

# SPECIFY .mongo file
filename = 'McGillX-CHEM181x-1T2014-prod.mongo'