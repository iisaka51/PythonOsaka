from c002_watcher import MyWatcher, FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    count = 0

    def on_any_event(self, event):
        if not event.is_directory:
            if MyHandler.count <10:
                with open(event.src_path, "a") as fp:
                    fp.write(f"{MyHandler.count} MODIFIED\n")
                    MyHandler.count += 1

if __name__=="__main__":
    w = MyWatcher(".", MyHandler())
    w.run()
