d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)

v1 = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

def func(data):
    for d in data:
        print(f'{d.name}  {d.birthday}')

# func(v1)
# print(v1)
