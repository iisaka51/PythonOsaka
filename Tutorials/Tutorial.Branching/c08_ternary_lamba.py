import random

a = random.random()
b = random.random()
c = (lambda: f"a:{a}", lambda: f"b:{b}")[a>b]()
