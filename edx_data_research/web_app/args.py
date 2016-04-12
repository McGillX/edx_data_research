from collections import namedtuple


ProblemIdsReport = namedtuple('ProblemIdsReport', ['db_name', 'uri', 'problem_ids',
                                                   'final_attempt', 'include_email',
                                                   'start_date', 'end_date',
                                                   'output_directory', 'row_limit',
                                                   'anonymize', 'display_names'])

SendEmail = namedtuple('SendEmail', ['from_address', 'from_name', 'password',
                                     'to_address', 'body', 'subject', 'attachments'])
