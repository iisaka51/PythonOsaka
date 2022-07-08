from contextlib import contextmanager

@contextmanager
def MyOpen(filename):
    try:
        file = open(filename, 'r')
        yield file
    finally:
        file.close()

with MyOpen('data.txt') as f:
     f.read()
