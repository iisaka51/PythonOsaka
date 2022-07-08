import random

a = random.random()
b = random.random()

decision_table = { False: f'F: {a}, b:{b}', True: f'T: {a}, b:{b}' }
c = decision_table[ all([a%2==0, b%2==0]) ]
d = decision_table[ any([a%2==0, b%2==0]) ]
