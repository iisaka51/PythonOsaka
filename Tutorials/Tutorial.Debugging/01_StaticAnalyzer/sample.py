class ClassA(object):
   def __init__(self, name):
         self.name = name
   def __repr__(self):
       return f'ClassA(name="{self.name}")'

class ClassB(object):
   def __init__(self, name):
         self.name = name
   def __repr__(self):
       return f'ClassB(name="{self.name}")'

class ClassC(object):
    def __init__(self):
        self.object_b = ClassB()
    def perform(self):
        self.object_a = ClassA()
