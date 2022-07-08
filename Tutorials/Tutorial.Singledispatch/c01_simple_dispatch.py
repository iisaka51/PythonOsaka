from typing import Any, List

def fun(arg: Any) -> str:
    if isinstance(arg, int):
        return 'int'
    elif isinstance(arg, list):
        return 'list'
    else:
        return 'default'

assert fun(1) == 'int'
assert fun([]) == 'list'
assert fun('str') == 'default'
