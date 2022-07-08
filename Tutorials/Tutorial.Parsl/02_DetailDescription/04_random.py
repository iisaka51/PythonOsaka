import random
factor = 5

def ambiguous_double(x):
     return x * random.random() * factor

num = ambiguous_double(42)
print(num)
