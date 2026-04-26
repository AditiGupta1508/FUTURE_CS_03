# Task 3 - File System Monitoring Tool
# Internship Project - Aditi Gupta

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging

# Configure logging to log file activity.
logging.basicConfig(
    filename="file_activity_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"Created: {event.src_path}")
        print(f"Created: {event.src_path}")

    def on_modified(self, event):
        logging.info(f"Modified: {event.src_path}")
        print(f"Modified: {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"Deleted: {event.src_path}")
        print(f"Deleted: {event.src_path}")

if __name__ == "__main__":
    path = "." # Monitor current directory, change as needed.
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring started on: {path}")
    print("Press CTRL+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 