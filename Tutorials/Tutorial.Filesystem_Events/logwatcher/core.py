from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from checker import FileChecker
from utils import get_timestamp
from typing import Tuple, List, Optional

class LogHandler(FileSystemEventHandler):

    def __init__(self,
                 watch_suffixes: Tuple[str] = ('.log'),
                 watch_pattern: List[str] = [],
                 watch_observate: bool = False
        ):
        self.watch_suffixes = watch_suffixes
        self.watch_pattern = watch_pattern
        self.watch_observate = watch_observate
        self.filechecker = FileChecker(self.watch_pattern)

    def on_any_event(self, event: FileSystemEvent):
        timestamp = get_timestamp()

        if not event.is_directory:
            path = event.src_path
            if hasattr(event, 'dest_path'):
                path = event.dest_path
            if path.endswith(self.watch_suffixes):
                basemsg = f"{timestamp}, {event.event_type}, File:{path}"
                for msg in self.filechecker.check_pattern(path=path):
                    print(f"{basemsg} {mg}")
        elif self.watch_observate:
            msg = f"{timestamp}, {event.event_type}, Dir:{event.src_path}"
            print(msg)

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass


class LogWatcher:
    observer = None
    stop_signal = 0

    def __init__(self,
                 watch_directory: str,
                 watch_interval: int,
                 watch_recursive: bool = False,
                 watch_suffixes: Tuple[str] = ['.log'],
                 watch_do_observate: bool = True,
                 watch_pattern: List[str] = list
        ):

        self.watch_directory = watch_directory
        self.watch_interval = watch_interval
        self.watch_recursive = watch_recursive
        self.watch_suffixes = watch_suffixes
        self.watch_do_observate = watch_do_observate
        self.watch_pattern = watch_pattern

        self.observer = Observer()
        self.event_handler = LogHandler(
            watch_suffixes, watch_pattern, watch_pattern)

    def schedule(self):
        self.observer.schedule(
            self.event_handler,
            self.watch_directory,
            recursive=self.watch_recursive)

    def start(self):
        self.schedule()
        timestamp = get_timestamp()
        msg = f"Logwatcher: {self.observer.name} - Started On: {timestamp}"
        print(msg)

        recurse = 'Recursively' if self.watch_recursive else 'Non-Recursively'
        msg = (
            f"Watching {recurse}"
            f", Suffix:{self.watch_suffixes}"
            f", Dir:{self.watch_recursive}"
            f", Interval:{self.watch_interval}(sec)"
            f", Patterns:'{self.watch_pattern}'"
        )
        print(msg)
        self.observer.start()

    def run(self):
        print("Logwacher is running:", self.observer.name)
        self.start()
        try:
            while True:
                time.sleep(self.watch_interval)

                if self.stop_signal == 1:
                    print(
                        f"Logwatcher stopped: {self.observer.name} "
                        f" stop signal:{self.stop_signal}")
                    self.stop()
                    break
        except:
            self.stop()
        self.observer.join()

    def stop(self):
        print("Logwatcher Stopped:", self.observer.name)

        timestamp = get_timestamp()
        msg = f"Logwatcher: {self.observer.name} - Stopped On: {timestamp}"
        print(msg)
        self.observer.stop()
        self.observer.join()

    def info(self):
        info = {
            'observerName': self.observer.name,
            'watch_directory': self.watch_directory,
            'watch_interval': self.watch_interval,
            'watch_recursive': self.watch_recursive,
            'watch_suffixes': self.watch_suffixes,
        }
        return info
