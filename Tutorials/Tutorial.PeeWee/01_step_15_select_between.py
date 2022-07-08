v1 = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))

def func(data):
    for d in data:
        print(f'{d.name}  {d.birthday}')

# func(v1)
# print(v1)
