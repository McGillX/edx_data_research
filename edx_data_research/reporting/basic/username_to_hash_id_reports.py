'''
In this script, we take a csv report as input and maps usernames
to their hash ids and return a new csv_report

Usage:
python username_to_hash_id_reports.py db_name csv_report

'''
import sys
import csv

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV 

db_name = sys.argv[1]

# Change name of collection as required
connection = EdXConnection(db_name, 'user_id_map' )
collection = connection.get_access_to_collection()

with open(sys.argv[2]) as f:
    headers = next(f)
    reader = csv.reader(f)
    data = [row for row in reader]

result = []
for row in data:
    username = row[0]
    if username.isdigit():
        username = int(username)
    cursor = collection['user_id_map'].find_one({'username' : username})
    if cursor:
        hash_id = cursor['hash_id']
        user_id = cursor['id']
        result.append([username, user_id, hash_id] + row[1:])
    else:
        print "username {0} not in collection".format(row[0])

input_file, extension = sys.argv[2].split('.')
output = CSV(result, [headers.split(',')[0],'User ID','User Hash ID'] + headers.split(',')[1:], output_file=input_file+'_username_anon.'+extension)
output.generate_csv()
