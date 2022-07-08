import sys
import functools

log_critical = functools.partial(print, file=sys.stderr)

log_critical('Hello World.')
# print('Hello World.', file=sys.stderr)
