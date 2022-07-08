"""
Usage:

from context_debug import debug

with debug():
    raise Exception("now testing")
"""

from contextlib import contextmanager

@contextmanager
def debug(use_pdb=True):
    try:
        yield
    except Exception as e:
        if not use_pdb:
            raise
        import sys
        import traceback
        import pdb
        info = sys.exc_info()
        traceback.print_exception(*info)
        pdb.post_mortem(info[2])

