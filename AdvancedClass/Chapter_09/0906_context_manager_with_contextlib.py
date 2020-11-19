import contextlib

@contextlib.contextmanager
class MyOpen():
    def __init__(self, filename):
        print('init() called')
        self.filename = filename

    def __enter__(self):
        print('enter() called')
        self.file = open(self.filename, 'r')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exit() called')
        self.file.close()


with MyOpen('data.txt') as manager:
    print('with statement block')
