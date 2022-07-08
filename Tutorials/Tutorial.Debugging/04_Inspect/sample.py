# https://t2y.hatenablog.jp/entry/20090909/1252474203

stack_content = [
    'frame obj  ',
    'file name  ',
    'line num   ',
    'function   ',
    'context    ',
    'index      ',
    ]

def get_inspect_stack():
    context, frame = 1, 2
    return dict(zip(stack_content, inspect.stack(context)[frame]))

def my_func():
    log.debug(pformat(get_inspect_stack()))
    def my_nested_func():
        log.debug("Current line  : %s", inspect.currentframe().f_lineno)
        log.debug(pformat(get_inspect_stack()))
        log.debug("Caller's line : %s", inspect.currentframe().f_back.f_lineno)
        def my_double_nested_func():
            log.debug(pformat(get_inspect_stack()))
        my_double_nested_func()
    my_nested_func()

