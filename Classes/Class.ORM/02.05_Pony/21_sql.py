x = 25
v1 = Person.select_by_sql('SELECT * FROM Person p WHERE p.age < $x')

# print(v1)
