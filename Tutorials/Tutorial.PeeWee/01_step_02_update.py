grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

v1 = grandma.name
grandma.name = 'Grandma L.'
v2 = grandma.save()
v3 = grandma.name

# print(grandma)
# print(herb)
# print(v1)
# print(v2)
# print(v3)
