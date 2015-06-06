'''
This module gets all the navigation events for each user while they are taking a test
'''
from collections import defaultdict
import time
from datetime import datetime

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

connection = EdXConnection('format_tests', 'tracking')
collection = connection.get_access_to_collection()
cursor = collection['format_tests'].find()
users_sessions = defaultdict(list)

for index,item in enumerate(cursor):
    #print index, item['parent_data']['chapter_display_name']
    users_sessions[(item['username'], item['session'])].append(item['time'])
users_tests_events = defaultdict(int)
for (username,session),times in users_sessions.iteritems():
    end_time = datetime.strptime(max(times).split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
    start_time = datetime.strptime(min(times).split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
    cursor = collection['tracking'].find({'username' : username, 'session' : session, '$or' : [{'event_type' : 'seq_goto'},{'event_type':'seq_prev'},{'event_type' : 'seq_next'}]})
    try:
        for index, document in enumerate(cursor):
            time_stamp = datetime.strptime(document['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
            if start_time <= time_stamp <= end_time:
            #print username, session, document['parent_data']#['chapter_display_name']    
                users_tests_events[(username, session, document['parent_data'].get('chapter_display_name', None),document['parent_data'].get('sequential_display_name', None))] += 1
    except:
        pass
    #break
result = []
for (username,session,chapter_name, sequential_name) in users_tests_events:
    result.append([username,session,chapter_name, sequential_name, users_tests_events[(username,session,chapter_name, sequential_name)]])

output = CSV(result, ['Username', 'Session ID', 'Chapter Display Name', 'Sequential Display Name', 'Navigation Count'], output_file='tests_analysis.csv')
output.generate_csv()
