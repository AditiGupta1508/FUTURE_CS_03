# ============================================================
# File System Monitoring Tool - Enhanced v2
# Author: Aditi Gupta | Cybersecurity Internship Project
# Features: Real-time monitoring, suspicious file detection,
#           event statistics, custom folder selection
# ============================================================

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
import os
from datetime import datetime

# ── CONFIGURATION ────────────────────────────────────────────
# File extensions that are potentially dangerous
SUSPICIOUS_EXTENSIONS = [
    '.exe', '.bat', '.sh', '.ps1', '.dll',
    '.vbs', '.cmd', '.msi', '.scr', '.jar'
]

# Log file name with timestamp so each session has its own log
LOG_FILE = f"file_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# ── LOGGING SETUP ─────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Also print logs to console (screen) at the same time
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# ── EVENT COUNTER ─────────────────────────────────────────────
# Tracks how many events happened in this session
event_stats = {
    "created": 0,
    "modified": 0,
    "deleted": 0,
    "suspicious": 0
}

# ── EVENT HANDLER ─────────────────────────────────────────────
class MonitorHandler(FileSystemEventHandler):

    def is_suspicious(self, path):
        """Check if the file has a suspicious extension."""
        _, ext = os.path.splitext(path)
        return ext.lower() in SUSPICIOUS_EXTENSIONS

    def on_created(self, event):
        event_stats["created"] += 1

        if self.is_suspicious(event.src_path):
            event_stats["suspicious"] += 1
            logging.warning(f"⚠️  SUSPICIOUS FILE CREATED: {event.src_path}")
            print(f"\n{'='*60}")
            print(f"  🚨 ALERT: Suspicious file detected!")
            print(f"  Path: {event.src_path}")
            print(f"{'='*60}\n")
        else:
            logging.info(f"[CREATED]  {event.src_path}")

    def on_modified(self, event):
        event_stats["modified"] += 1

        if self.is_suspicious(event.src_path):
            event_stats["suspicious"] += 1
            logging.warning(f"⚠️  SUSPICIOUS FILE MODIFIED: {event.src_path}")
        else:
            logging.info(f"[MODIFIED] {event.src_path}")

    def on_deleted(self, event):
        event_stats["deleted"] += 1
        logging.info(f"[DELETED]  {event.src_path}")

# ── STATS DISPLAY ─────────────────────────────────────────────
def print_stats():
    """Print a summary of all events when monitoring stops."""
    print("\n" + "="*60)
    print("         📊 SESSION SUMMARY")
    print("="*60)
    print(f"  ✅ Files Created:      {event_stats['created']}")
    print(f"  ✏️  Files Modified:     {event_stats['modified']}")
    print(f"  ❌ Files Deleted:      {event_stats['deleted']}")
    print(f"  ⚠️  Suspicious Events:  {event_stats['suspicious']}")
    print(f"  📁 Log saved to:       {LOG_FILE}")
    print("="*60)

# ── MAIN PROGRAM ──────────────────────────────────────────────
if __name__ == "__main__":
    print("="*60)
    print("   🔍 File System Monitoring Tool - Enhanced v2")
    print("   Author: Aditi Gupta | Cybersecurity Project")
    print("="*60)

    # Let user choose which folder to monitor
    path = input("\nEnter folder path to monitor (or press Enter for current directory): ").strip()
    if not path:
        path = "."
    
    # Validate the path exists
    if not os.path.exists(path):
        print(f"❌ Error: Path '{path}' does not exist.")
        exit(1)

    print(f"\n✅ Monitoring started on: {os.path.abspath(path)}")
    print(f"📄 Logging to: {LOG_FILE}")
    print(f"🚨 Watching for suspicious extensions: {', '.join(SUSPICIOUS_EXTENSIONS)}")
    print("\nPress CTRL+C to stop monitoring...\n")

    # Start the observer
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    logging.info(f"Monitoring started on: {os.path.abspath(path)}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoring stopped by user.")
        print_stats()

    observer.join()