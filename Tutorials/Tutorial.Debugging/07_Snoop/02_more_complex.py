import snoop

def cache(func):
    d = {}

    def wrapper(*args):
        try:
            return d[args]
        except KeyError:
            result = d[args] = func(*args)
            return result

    return wrapper

@snoop(depth=2)
@cache
def add(x, y):
    return x + y

# add(1, 2)
# add(1, 2)
