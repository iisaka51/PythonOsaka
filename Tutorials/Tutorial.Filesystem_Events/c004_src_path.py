from pathlib import Path
from c002_watcher import MyWatcher, FileSystemEventHandler

class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.event_type == "deleted":
            filename = Path(event.src_path).absolute()
            print(f"{filename} was deleted.")

if __name__=="__main__":
    w = MyWatcher(".", MyHandler())
    w.run()
