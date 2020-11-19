class Struct():
    pass


queen = Struct()
print(dir(queen))

queen.firstname = 'Freddie'
queen.lastname = 'Mercury'

whitesnake = Struct()
whitesnake.firstname = 'David'
whitesnake.lastname = 'Coverdale'

print(queen.firstname)
print(queen.lastname)
print(whitesnake.firstname)
print(whitesnake.lastname)

print(queen)
print(whitesnake)
