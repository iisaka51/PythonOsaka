from math import sqrt

def my_math(a, b):
    for v in map(sqrt, range(a, b)):
        print(v)
