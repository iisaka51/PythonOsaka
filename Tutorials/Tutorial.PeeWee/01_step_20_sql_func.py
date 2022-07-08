expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
v1 = Person.select().where(expression)

def func(data):
    for d in data:
        print(f'{d.name}')

# func(v1)
# print(v1)
# print(expression)
