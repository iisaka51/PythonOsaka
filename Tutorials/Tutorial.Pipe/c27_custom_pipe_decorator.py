from pipe import Pipe

@Pipe
def first(x):
    return next(iter(x))

v1 = [1, 2, 3] | first

# v1
