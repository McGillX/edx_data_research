'''
This module gathers the number of various categories under each sequential including
the number of html, videos, verticals etc.

Usage:

python sequential_aggregation.py

'''
from collections import defaultdict

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

connection = EdXConnection('course_structure')
collection = connection.get_access_to_collection()
cursor = collection['course_structure'].find({'category' : 'sequential'})
result = []
for index, item in enumerate(cursor):
    children = item['children']
    temp_result = [item['_id'], item['parent_data']['chapter_display_name'],item['metadata']['display_name'], len(children)]
    aggregate_vertical = defaultdict(int)
    aggregate_category= defaultdict(int)
    for _id in children:
        try:
            vertical = collection['course_structure'].find_one({'_id' : _id})
            aggregate_vertical[vertical['category']] += 1
            for _id in vertical['children']:
                child = collection['course_structure'].find_one({'_id' : _id})
                aggregate_category[child['category']] += 1
        except Exception:
           pass
    temp_result.extend([aggregate_category['video'], aggregate_category['html'], aggregate_category['problem'],aggregate_category['discussion'],aggregate_category['poll_question'],aggregate_category['word_cloud']])
    result.append(temp_result)

output = CSV(result, ['Sequential ID', 'Chapter Display Name' ,'Sequential Name', 'Number of Verticals', 'Number of Videos', 'Number of HTML','Number of Problems' ,'Number of Discussions', 'Number of Poll Questions', 'Number of Word Cloud'], output_file='sequential_aggregation.csv')
output.generate_csv()
