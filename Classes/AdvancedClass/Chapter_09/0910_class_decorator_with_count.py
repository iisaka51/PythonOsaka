# 単純なクラス継承
class Base:
    familyname = 'jackson'

class Father(Base):
    pass

class Mother(Base):
    pass

class Child(Father, Mother):
    pass

print(Father.familyname)
print(Mother.familyname)
print(Child.familyname)
