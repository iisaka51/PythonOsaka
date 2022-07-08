from dataclasses import dataclass

@dataclass
class A:
    a: int
    b: str

@dataclass
class B:
    c: str
    d: A

data ={'c':'hello', 'd':{'a':4, 'b':'bye'}}
v1 = B(**data)

data ={'c':'hello', 'd': A(**{'a':4, 'b':'bye'})}
v2 = B(**data)

# print(v1)
# print(v2)
