v1 = Pet.select().join(Person).where(Person.name == 'Bob')

def func(data):
    for d in data:
        print(f'{d.name}')

# func(v1)
# print(v1)
