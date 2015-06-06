from collections import defaultdict
import json
import sys 

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV 

db_name = sys.argv[1]

# Change name of collection as required
connection = EdXConnection(db_name, 'forum' )
collection = connection.get_access_to_collection()

forum_data = collection['forum'].find() 
csv_data = []
for document in forum_data:
    csv_data.append([document['_id'], document['author_username'], document['_type'], document.get('title', ''), document['body'], document['created_at']])

headers = ['ID', 'Author Username', 'Type', 'Title', 'Body', 'Created At Date']
output = CSV(csv_data, headers, output_file=db_name+'_forum_data.csv')
output.generate_csv()
