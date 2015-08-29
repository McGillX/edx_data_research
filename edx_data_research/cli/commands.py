"""
In this module we define the interface between the cli input provided
by the user and the analytics required by the user
"""
from edx_data_research.reporting.basic import (user_info, ip_to_country,
                                               course_completers)
from edx_data_research.reporting.edx_base import EdX
from edx_data_research.reporting.problem_ids.problem_ids import (ProblemIds,
                                                                problem_ids)


def cmd_list(args):
    """
    List all the analytics commands and their summary
    """
    print 'list all'
	
def cmd_report_basic(args):
    """
    Run basic analytics
    """
    edx_obj = EdX(args)
    globals()[args.basic.replace('-', '_')](edx_obj)

def cmd_report_problem_ids(args):
    edx_obj = ProblemIds(args)
    problem_ids(edx_obj)
