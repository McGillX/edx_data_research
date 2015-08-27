'''
In this module, we will generate a csv report for a given problem id, which
will include information about how students fared with a given problem id

'''
from itertools import groupby

from edx_data_research.reporting.edx_base import EdX


class ProblemId(EdX):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        self.problem_id = args.problem_id
        self.final_attempt = args.final_attempt

def _generate_name_from_problem_id(problem_id, display_name, final_attempt):
    '''Generate name of csv output file from problem id'''
    attempts_name = '_FinalAttempts' if final_attempt else '_AllAttempts'
    return ('_'.join(problem_id.split('/')[3:]) + '_' +
            ''.join(e for e in display_name if e.isalnum()) + attempts_name +
            '.csv')

def problem_id(edx_obj):
    edx_obj.collections = ['problem_ids']
    cursor = edx_obj.collections['problem_ids'].find({'event.problem_id' :
                                                     edx_obj.problem_id})
    display_name = cursor[0]['module']['display_name']
    one_record = cursor[0]['event']
    problem_ids_keys = sorted(one_record['correct_map'].keys(),
                              key=lambda x : int(x.split('_')[-2]))
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
        for key in sorted(document['event']['correct_map'].keys(),
                          key=lambda x : int(x.split('_')[-2])):
            try:
                answers.append(document['event']['submission'][key]['answer'])
            except KeyError:
                answers.append('')
        result.append([document['hash_id'], document['username'],
                       document['event']['attempts'],
                       document['module']['display_name'], document['time'],
                       document['event']['success'], document['event']['grade'],
                       document['event']['max_grade']] + answers)
    if edx_obj.final_attempt:
        result = [max(items, key=lambda x : x[1]) for key, items in
                  groupby(sorted(result, key=lambda x : x[0]), lambda x : x[0])]
    csv_report_name = _generate_name_from_problem_id(edx_obj.problem_id,
                                                     display_name,
                                                     edx_obj.final_attempt)
    headers = (['Hash ID'] if edx_obj.anonymize else
               ['Hash ID', 'User ID', 'Username'])
    headers.extend(['Attempt Number', 'Module', 'Time', 'Success',
                    'Grade Achieved', 'Max Grade'])
    edx_obj.generate_csv(result, headers, csv_report_name)
