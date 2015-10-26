'''
In this module, we will generate a csv report for a given problem id, which
will include information about how students fared with a given problem id

'''
from itertools import groupby, izip_longest

from edx_data_research.reporting.edx_base import EdXReport


class ProblemIds(EdXReport):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        self._ids = args.problem_ids
        self.final_attempt = args.final_attempt
        self.display_names = args.display_names or []
    
    def report_name(self, *args):
        '''Generate name of csv output file from problem id'''
        attempts_name = '-FinalAttempts' if args[2] else '-AllAttempts'
        display_name = '-' + args[1].replace(':', '').replace(' ', '_')
        return ('-'.join(arg.lower() for arg in args[0].split('/')[3:]) +
                display_name + attempts_name + '.csv')

    @staticmethod
    def _problem_id_questions(answer_map):
        problem_id_keys = sorted(answer_map.keys(),
                                 key=lambda x : int(x.split('_')[-2]))
        problem_id_questions = []
        for key in problem_id_keys:
            try:
                item = answer_map['submission'][key]
                value = item['question']
                problem_id_questions.append('{0} : {1}'.format(key, value))
            except UnicodeEncodeError:
                value = value.encode("utf-8")
                problem_id_questions.append('{0} : {1}'.format(key, value))
            except KeyError:
                problem_id_questions.append('{0}'.format(key))
        return problem_id_questions

    def problem_ids(self):
        '''Retrieve information about how students fared for a given problem id'''
        self.collections = ['problem_ids']
        for problem_id, display_name in izip_longest(self._ids,
                                                     self.display_names,
                                                     fillvalue=''):
            cursor = self.collections['problem_ids'].find({'event.problem_id' :
                                                          problem_id})
            display_name = display_name or cursor[0]['module']['display_name']
            one_record = cursor[0]['event']['correct_map']
            problem_id_questions = self.__class__._problem_id_questions(one_record)
            result = []
            for document in cursor:
                answers = []
                for key in sorted(document['event']['correct_map'].keys(),
                                  key=lambda x : int(x.split('_')[-2])):
                    try:
                        answers.append(document['event']['submission'][key]['answer'])
                    except KeyError:
                        answers.append('')
                row = self.anonymize_row([document['hash_id']],
                                         [document['user_id'],
                                          document['username']],
                                         [document['event']['attempts'],
                                          document['time'],
                                          document['event']['success'],
                                          document['event']['grade'],
                                          document['event']['max_grade']] +
                                          answers)
                result.append(row)
            if self.final_attempt:
                result = [max(items, key=lambda x : x[1]) for key, items in
                          groupby(sorted(result, key=lambda x : x[0]),
                          lambda x : x[0])]
            csv_report_name = self.report_name(problem_id, display_name,
                                               self.final_attempt)
            headers = self.anonymize_headers(['Attempt Number', 'Time',
                                              'Success', 'Grade Achieved',
                                              'Max Grade'] + 
                                              problem_id_questions)
            self.generate_csv(result, headers, csv_report_name)
