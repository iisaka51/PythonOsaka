from functools import singledispatch
from typing import Any, List

@singledispatch
def func(arg: Any) -> str:
    return 'default'

@func.register(int)
def func_int(arg: int) -> str:
        return 'int'

@func.register(list)
def func_list(arg: List) -> str:
        return 'list'

assert func(1) == 'int'
assert func([]) == 'list'
assert func('str') == 'default'
