import ZODB.utils

class Lock:
    def acquire(self):
        print('acquire')
    def release(self):
        print('release')
    def __enter__(self):
        return self.acquire()
    def __exit__(self, *ignored):
        return self.release()
