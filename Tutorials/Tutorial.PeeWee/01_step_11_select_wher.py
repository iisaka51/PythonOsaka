v1 = Pet.select().where(Pet.owner == uncle_bob)

def func(data):
    for d in data:
        print(f'{d.name}')

# func(v1)
# print(v1)
