import ZODB
from persistent import Persistent

class Member(Persistent):
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name

