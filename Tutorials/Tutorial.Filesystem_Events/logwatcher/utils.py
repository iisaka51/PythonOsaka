import datetime
from pathlib import Path

def get_timestamp():
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def is_dir_path(path):
    if Path(path).is_dir():
        return path
    else:
        raise NotADirectoryError(path)
