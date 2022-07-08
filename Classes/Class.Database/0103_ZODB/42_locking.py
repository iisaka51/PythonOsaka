from zodb_precondition import *

class C:
    _lock = Lock()
    _lock_acquire = _lock.acquire
    _lock_release = _lock.release

    @ZODB.utils.locked
    def meth(self, *args, **kw):
        print('meth %r %r' %(args, kw))

# C().meth(1, 2, a=3)
