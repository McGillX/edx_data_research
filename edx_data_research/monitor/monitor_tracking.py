import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

class TrackingEventHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1]
    else:
        raise ValueError('Missing path to directory to monitor!!!')
    event_handler = TrackingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
