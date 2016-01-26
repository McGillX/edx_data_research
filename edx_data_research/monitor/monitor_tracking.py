import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler 

class TrackingLogHandler(PatternMatchingEventHandler):

    def on_created(self, event):
        print event.__repr__()
        print event.event_type, event.is_directory, event.src_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        raise ValueError('Missing path to directory to monitor!!!')
    event_handler = TrackingLogHandler(['*.log'], ['*.log-errors'],
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
