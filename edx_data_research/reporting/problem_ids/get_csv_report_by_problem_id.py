'''
In this module, we will generate a csv report for a given problem id, which
will include information about how students fared with a given problem id

Usage:

from the reporting directory

python -m problem_ids.get_csv_report_by_problem_id <db_name> <problem_id> [--max-attempt]

Example:

 python -m problem_ids.get_csv_report_by_problem_id body101x i4x://McGillX/Body101x/problem/fd3a83b0c06243b78554b69ad6f65e03


'''
import sys

from itertools import groupby

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

if len(sys.argv) < 3:
    usage_message = """
    No problem id given as a command line argument. Please provide a problem_id

    Usage:
    python get_csv_report_by_problem_id.py <db_name> <problem_id> [--final_attempts]

    """

    sys.stderr.write(usage_message)
    sys.exit(1)

db_name = sys.argv[1]
problem_id = sys.argv[2]
final_attempts = True if len(sys.argv) == 4  else False
connection = EdXConnection(db_name, 'problem_ids')
collection = connection.get_access_to_collection()

def _generate_name_from_problem_id(problem_id, display_name):
    '''Generate name of csv output file from problem id'''
    attempts_name = '_AllAttempts'
    if final_attempts: 
        attempts_name = '_FinalAttempts'
    return ('_'.join(problem_id.split('/')[3:]) + '_' +
            ''.join(e for e in display_name if e.isalnum()) + attempts_name + '.csv')

cursor = collection['problem_ids'].find({'event.problem_id': problem_id})
display_name = cursor[0]['module']['display_name']
one_record = cursor[0]['event']
problem_ids_keys = sorted(one_record['correct_map'].keys())
problem_ids = []
for key in problem_ids_keys:
    try:
        item = one_record['submission'][key]
        value = item['question']
        problem_ids.append('{0} : {1}'.format(key, value))
    except UnicodeEncodeError:
        value = value.encode("utf-8")
        problem_ids.append('{0} : {1}'.format(key, value))
    except KeyError:
        problem_ids.append('{0}'.format(key))
result = []
for document in cursor:
    answers = []
    for key in sorted(document['event']['correct_map'].keys()):
        try:
            answers.append(document['event']['submission'][key]['answer'])
        except KeyError:
            answers.append('')
    result.append([document['username'], document['event']['attempts'],
                   document['module']['display_name'],document['time'],
                   document['event']['success'],
                   document['event']['grade'], document['event']['max_grade']]
                   + answers)

if final_attempts:
    result = [max(items, key=lambda x : x[1]) for key, items in
              groupby(sorted(result, key=lambda x : x[0]), lambda x : x[0])] 

csv_report_name = _generate_name_from_problem_id(problem_id, display_name)
output = CSV(result,
             ['Username', 'Attempt Number', 'Module', 'Time', 'Success', 'Grade Achieved', 'Max Grade'] + problem_ids,
             output_file=csv_report_name)
output.generate_csv()
