import csv
import os
import sys
import time
from collections import namedtuple

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler 

from edx_data_research.parsing.parse_tracking import Tracking

Args = namedtuple('Args', ['db_name', 'uri', 'logs'])

REPORT_NAME = '/data/tracking_logs_monitoring_report.csv'

def update_report(result):
    path_to_report = os.path.join(os.path.expanduser('~'), REPORT_NAME)
    with open(path_to_report, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(result)

class TrackingLogHandler(PatternMatchingEventHandler):

    def on_created(self, event):
        print event.__repr__()
        args = Args('tracking', 'localhost', [event.src_path])
        edx_obj = Tracking(args)
        result = edx_obj.migrate()
        update_report(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        raise ValueError('Missing path to directory to monitor!!!')
    event_handler = TrackingLogHandler(['*.log', '*.log.gz'], ['*.log-errors'],
                                       case_sensitive=True)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
