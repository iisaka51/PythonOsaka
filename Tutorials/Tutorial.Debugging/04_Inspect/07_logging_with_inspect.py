import inspect
import logging
from models import User
from pprint import pprint, pformat

stack_content = [
    'frame obj  ',
    'file name  ',
    'line num   ',
    'function   ',
    'context    ',
    'index      ',
    ]

LOG_FILENAME = 'logging_example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("__name__")

def get_inspect_stack():
    context, frame = 1, 2
    return dict(zip(stack_content, inspect.stack(context)[frame]))

def outer_func():
    log.debug(pformat(get_inspect_stack()))
    def inner_func():
        log.debug("Current line  : %s", inspect.currentframe().f_lineno)
        log.debug(pformat(get_inspect_stack()))
        log.debug("Caller's line : %s", inspect.currentframe().f_back.f_lineno)
        def inner_inner_func():
            log.debug(pformat(get_inspect_stack()))
        inner_inner_func()
    inner_func()

def main():
    user = User(first_name='David', last_name='Coverdale')
    outer_func()

if __name__ == '__main__':
    main()
