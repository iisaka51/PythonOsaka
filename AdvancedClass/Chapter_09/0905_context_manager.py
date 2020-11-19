class MyContextManager():
    def __init__(self):
        print('init() called')

    def __enter__(self):
        print('enter() called')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exit() called')


with MyContextManager() as manager:
    print('with statement block')
