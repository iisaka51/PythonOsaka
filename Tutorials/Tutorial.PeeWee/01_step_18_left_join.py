v1 = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))

def func(data):
    for d in data:
        if hasattr(d, 'pet'):
            print(f'{d.name} {d.pet.name}')
        else:
            print(f'{d.name} no pets')

# func(v1)
# print(v1)
