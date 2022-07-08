v1 = Person.select()

def func(data):
    for d in data:
        print(f'{d.name} {d.pets.count()} pets')

# func(v1)
# print(v1)
