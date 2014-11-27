'''
This module determines how many chapters were accessed by each user for a 
given course

Usage:

python chapters_accessed_per_user

'''


from base_edx import EdXConnection
from generate_csv_report import CSV 

connection = EdXConnection('tracking', 'course_structure')
collection = connection.get_access_to_collection()

# Get all chapters
chapters = collection['course_structure'].distinct('parent_data.chapter_display_name')

