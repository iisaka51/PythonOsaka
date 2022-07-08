from typing import Any, List

try:
    # python 3.8 or later
    from functools import singledispatchmethod
except ImportError:
    from functools import singledispatch, update_wrapper

    def singledispatchmethod(func):
        dispatcher = singledispatch(func)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, func)
        return wrapper

class Patchwork(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @singledispatchmethod
    def get(self, arg: Any) -> Any:
        return getattr(self, arg, None)

    @get.register(list)
    def _get_list(self, arg: List) -> List:
        return [self.get(x) for x in arg]

if __name__ == '__main__':
    pw = Patchwork(a=1, b=2, c=3)
    print(pw.get('b'))
    print(pw.get(['a', 'c']))
