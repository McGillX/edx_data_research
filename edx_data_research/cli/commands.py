"""
In this module we define the interface between the cli input provided
by the user and the analytics required by the user
"""
from edx_data_research import parsing
from edx_data_research import reporting

def cmd_report_basic(args):
    """
    Run basic analytics
    """
    edx_obj = reporting.Basic(args)
    getattr(edx_obj, args.basic.replace('-', '_'))()

def cmd_report_problem_ids(args):
    edx_obj = reporting.ProblemIds(args)
    getattr(edx_obj, args.report.replace('-', '_'))()

def cmd_report_stats(args):
    edx_obj = reporting.Stats(args)
    getattr(edx_obj, args.report.replace('-', '_'))()

def cmd_parse_sql(args):
    edx_obj = parsing.SQL(args)
    edx_obj.migrate()

def cmd_parse_forum(args):
    edx_obj = parsing.Forum(args)
    edx_obj.migrate()

def cmd_parse_problem_ids(args):
    edx_obj = parsing.ProblemIds(args)
    edx_obj.migrate()

def cmd_parse_course_structure(args):
    edx_obj = parsing.CourseStructure(args)
    edx_obj.migrate()
