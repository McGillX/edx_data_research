"""
In this module we define the interface between the cli input provided
by the user and the analytics required by the user
"""
from edx_data_research.parsing.forum.parse_forum import Forum
from edx_data_research.parsing.problem_ids.problem_ids_collection import ProblemIdsCollection
from edx_data_research.parsing.sql.parse_sql import SQL
from edx_data_research.reporting.edx_basic import Basic
from edx_data_research.reporting.edx_problem_ids import ProblemIds
from edx_data_research.reporting.edx_stats import Stats


def cmd_report_basic(args):
    """
    Run basic analytics
    """
    edx_obj = Basic(args)
    getattr(edx_obj, args.basic.replace('-', '_'))()

def cmd_report_problem_ids(args):
    edx_obj = ProblemIds(args)
    getattr(edx_obj, args.report.replace('-', '_'))()

def cmd_report_stats(args):
    edx_obj = Stats(args)
    getattr(edx_obj, args.report.replace('-', '_'))()

def cmd_parse_sql(args):
    edx_obj = SQL(args)
    edx_obj.migrate()

def cmd_parse_forum(args):
    edx_obj = Forum(args)
    edx_obj.migrate()

def cmd_parse_problem_ids(args):
    edx_obj = ProblemIdsCollection(args)
    edx_obj.migrate()
