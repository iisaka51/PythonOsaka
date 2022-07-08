v1 = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

def func(data):
    for d in data:
        print(f'{d.name} {d.owner.name}')

# func(v1)
# print(v1)
