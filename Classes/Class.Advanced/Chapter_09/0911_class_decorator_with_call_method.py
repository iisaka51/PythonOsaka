# クラスのデコレータ
def decorator(cls):
    class  NewClass(cls):
        familyname = 'jackson'
    return NewClass

@decorator
class Father:
    pass

@decorator
class Mother:
    pass

class Child(Father, Mother):
    pass

print(Father.familyname)
print(Mother.familyname)
print(Child.familyname)
