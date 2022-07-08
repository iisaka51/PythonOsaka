import random

a = random.random()
b = random.random()

c = {False: f'b:{b}', True: f'a:{a}'}[a>b]
