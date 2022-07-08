persons = select(p for p in Person if 'o' in p.name)

def func(data):
    for d in data:
        print(d.name, d.age)

# print(persons)
# func(persons)
