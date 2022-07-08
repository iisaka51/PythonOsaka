v1 = Person.select().order_by(Person.name).prefetch(Pet)

def func(data):
    for d in data:
        print('{data.name}')
        for pet in d.pets:
            print(f'  * {d.name}')

# func(v1)
# print(v1)
