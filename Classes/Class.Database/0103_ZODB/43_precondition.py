from zodb_precondition import *

class C:
    def __init__(self):
        self._lock = Lock()
        self._opened = True
        self._transaction = None
    def opened(self):
        print('checking if open')
        return self._opened
    def not_in_transaction(self):
        print('checking if in a transaction')
        return self._transaction is None
    @ZODB.utils.locked(opened, not_in_transaction)
    def meth(self, *args, **kw):
        print('meth %r %r' % (args, kw))
c = C()
# c.meth(1, 2, a=3)
# c._transaction = 1
# c.meth(1, 2, a=3)
# c._opened = False
# c.meth(1, 2, a=3)

