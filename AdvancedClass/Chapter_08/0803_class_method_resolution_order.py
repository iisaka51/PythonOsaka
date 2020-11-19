class Father:
    id='father'

class Mother:
    id='mother'

class Child(Father, Mother):
    pass

print(Child.id)
print(issubclass(Child,Mother))
print(issubclass(Child,Father))

# MRO (Method Resolution Order)
print(Child.__mro__)
