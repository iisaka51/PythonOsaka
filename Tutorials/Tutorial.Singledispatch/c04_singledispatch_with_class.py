from functools import singledispatch
from typing import Any, List

class Patchwork(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @singledispatch
    def get(self, arg: Any) -> Any:
        return getattr(self, arg, None)

    @get.register(list)
    def _get_list(self, arg: List) -> List:
        return [self.get(x) for x in arg]

if __name__ == '__main__':
    pw = Patchwork(a=1, b=2, c=3)
    print(pw.get('b'))
    print(pw.get(['a', 'c']))