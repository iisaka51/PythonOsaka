ACTIONS = dict()

def register(func):
    ACTIONS[func.__name__] = func
    return func
