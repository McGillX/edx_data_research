from collections import namedtuple


BasicReport = namedtuple('BasicReport', ['db_name', 'uri', 'basic', 'anonymize',
                                         'output_directory', 'row_limit'])

GeneralStats = namedtuple('GeneralStats', ['db_name', 'uri', 'csv', 'anonymize',
                                           'output_directory', 'row_limit'])

ProblemIdsReport = namedtuple('ProblemIdsReport', ['db_name', 'uri', 'problem_ids',
                                                   'final_attempt', 'include_email',
                                                   'start_date', 'end_date',
                                                   'output_directory', 'row_limit',
                                                   'anonymize', 'display_names'])

SendEmail = namedtuple('SendEmail', ['from_address', 'from_name', 'password',
                                     'to_address', 'body', 'subject', 'attachments'])

SQL = namedtuple('SQL', ['db_name', 'uri', 'collection', 'sql_file'])

Forum = namedtuple('Forum', ['db_name', 'uri', 'forum_file'])

CourseStructure = namedtuple('CourseStructure', ['db', 'uri', 'course_structure_file', 'drop'])

CourseTracking = namedtuple('CourseTracking', ['db', 'uri', 'course_config_file', 'drop'])

ProblemIdsParse = namedtuple('ProblemIdsParse', ['db', 'uri', 'drop'])