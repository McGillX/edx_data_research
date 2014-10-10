'''
In this module, we will generate a csv report for a given problem id, which
will include information about how students fared with a given problem id

Usage:

python get_csv_report_by_problem_id.py <problem_id>

Example:

python get_csv_report_by_problem_id.py i4x://McGillX/ATOC185x/problem/dedc04b82b6e483b9c95dbe26313e5f3

'''
from collections import defaultdict
import sys

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('atoc185x_problem_ids')
collection = connection.get_access_to_collection()

if len(sys.argv) < 2:
    usage_message = """
    No problem id given as a command line argument. Please provide a problem_id

    Usage:
    python get_csv_report_by_problem_id.py <problem_id>

    """

    sys.stderr.write(usage_message)
    sys.exit(1)

def _generate_name_from_problem_id(problem_id):
    '''
    Generate name of csv output file from problem id
    '''
    return '_'.join(problem_id.split('/')[3:])

cursor = collection['atoc185x_problem_ids'].find({'event.problem_id':sys.argv[1]})
#cursor = collection['atoc185x_problem_ids'].aggregate([{'$match' : 
#{'problem_id':sys.argv[1]}}, {'$group' : { '_id' :  {'username' : '$username',
#'attempt_number' : '$event.attempts', 'time' : '$time','answers' : '$event.answers',
#'success' : '$event.success', 'grade' : '$event.grade', 'max_grade' : '$event.max_grade'}}}]) 

result = []
for document in cursor:
    result.append([document['username'], document['event']['attempts'], document['module']['display_name'],document['time'], document['event']['success'],
    document['event']['grade'], document['event']['max_grade'], document['event']['answers']])

csv_report_name = _generate_name_from_problem_id(sys.argv[1])
output = CSV(result, [], output_file=csv_report_name)
output.generate_csv()

