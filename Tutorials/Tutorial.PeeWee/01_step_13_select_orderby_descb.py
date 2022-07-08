v1 = Person.select().order_by(Person.birthday.desc())

def func(data):
    for d in data:
        print(f'{d.name} {d.birthday}')

# func(v1)
# print(v1)
