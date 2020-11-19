class Family:
    def __init__(self, name):
        self.name = name

# Father class inherited from Family
class Person(Family):
    def __init__(self, name, age):
        Family.__init__(self, name) # super().__iit__(name) と同じ
        self.age = age

f = Person("Freddie", 48)
print(f.name)
print(f.age)
