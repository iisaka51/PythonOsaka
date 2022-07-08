v1 = (Person
         .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
         .join(Pet, JOIN.LEFT_OUTER)
         .group_by(Person)
         .order_by(Person.name))

def func(data):
    for d in data:
        print(f'{d.name} {d.pet_count} pets')

# func(v1)
# print(v1)
