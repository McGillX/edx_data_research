'''
In this module, we will generate a csv report for a given problem id, which
will include information about how students fared with a given problem id

Usage:

python get_csv_report_by_problem_id.py <db_name> <problem_id>

Example:

python get_csv_report_by_problem_id.py atoc185x i4x://McGillX/ATOC185x/problem/dedc04b82b6e483b9c95dbe26313e5f3

'''
from collections import defaultdict
import sys

from common.base_edx import EdXConnection
from common.generate_csv_report import CSV

db_name = sys.argv[1]
problem_id = sys.argv[2]
connection = EdXConnection(db_name, 'problem_ids')
collection = connection.get_access_to_collection()

if len(sys.argv) < 3:
    usage_message = """
    No problem id given as a command line argument. Please provide a problem_id

    Usage:
    python get_csv_report_by_problem_id.py <db_name> <problem_id>

    """

    sys.stderr.write(usage_message)
    sys.exit(1)

def _generate_name_from_problem_id(problem_id):
    '''
    Generate name of csv output file from problem id
    '''
    return '_'.join(problem_id.split('/')[3:]) + '.csv'

cursor = collection['problem_ids'].find({'event.problem_id': problem_id})
result = []
for document in cursor:
    answers = {key : value['answer'] for key, value in document['event']['submission'].iteritems()}
    result.append([document['username'], document['event']['attempts'], document['module']['display_name'],document['time'], document['event']['success'],
    document['event']['grade'], document['event']['max_grade'], answers])

csv_report_name = _generate_name_from_problem_id(problem_id)
output = CSV(result, ['Username', 'Attempt Number', 'Module', 'Time', 'Success', 'Grade Achieved', 'Max Grade', 'Answers'], output_file=csv_report_name)
output.generate_csv()
