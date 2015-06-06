'''
This module gets the number of completers who did each activity
'''
import csv
from datetime import datetime
from collections import defaultdict
import sys

from common.base_edx import EdXConnection

connection = EdXConnection('tracking' )
collection = connection.get_access_to_collection()

with open('csv_files/McGillX_CHEM181x_1T2014_grade_report_2014-04-24-1030.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    #usernames = [row[2] for row in reader]
    usernames = [row[2] for row in reader]

cursor = collection['tracking'].aggregate([{'$match' : {'username' : {'$in' : usernames}}},{'$group' : { '_id' : { "chapter_name" : "$parent_data.chapter_display_name" ,"sequential_name" : "$parent_data.sequential_display_name","vertical_name" : "$parent_data.vertical_display_name"},'students' : {'$addToSet':"$username"}}}, {'$unwind' : "$students"} ,{'$group' : {'_id': "$_id",' num_of_students' : {'$sum' : 1}}}, {'$out' : sys.argv[1]}])
