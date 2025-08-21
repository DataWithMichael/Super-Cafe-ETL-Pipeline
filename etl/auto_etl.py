import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from create_tables import create_tables
from transformation import transform_and_load
import os

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../data")

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"📄 New CSV detected: {event.src_path}")
            transform_and_load(event.src_path)

def main():
    print("🚀 Starting ETL pipeline in watch mode...")
    create_tables()  # ensure tables exist

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, DATA_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("🛑 ETL pipeline stopped.")

if __name__ == "__main__":
    main()
