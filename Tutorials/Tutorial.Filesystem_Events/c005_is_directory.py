from pathlib import Path
from c002_watcher import MyWatcher, FileSystemEventHandler

class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        name = Path(event.src_path).name
        if event.is_directory:
            print(f"event occurred in directory: {name}.")
        else:
            print(f"event occurred in file: {name}.")

if __name__=="__main__":
    w = MyWatcher(".", MyHandler())
    w.run()
