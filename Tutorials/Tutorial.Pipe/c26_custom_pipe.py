from pipe import Pipe

first = Pipe(lambda iterable: next(iter(iterable)))
v1 = [1, 2, 3] | first

# v1
