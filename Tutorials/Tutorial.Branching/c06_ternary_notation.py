import random

a = random.random()
b = random.random()

c = (f'b:{b}', f'a:{a}')[a>b]
