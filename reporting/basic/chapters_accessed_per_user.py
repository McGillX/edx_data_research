'''
This module determines how many chapters were accessed by each user for a 
given course

Usage:

python chapters_accessed_per_user

'''
from collections import defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV 

connection = EdXConnection('tracking', 'course_structure')
collection = connection.get_access_to_collection()

# Get all chapters
chapters = collection['course_structure'].distinct('parent_data.chapter_display_name')

tracking = collection['tracking'].find()
result = []
for document in tracking:
    if 'parent_data' in document:
        pass
    
output = CSV(result, ['Username'].extend(chapters), output_file='atoc185x_chapters_accesses_per_user.csv')
output.generate_csv()

