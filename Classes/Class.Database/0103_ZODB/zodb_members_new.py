import ZODB
from persistent import Persistent

class Member(Persistent):
    def __init__(self):
        self.members = []
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def add_member(self, name):
        self.members.append(name)
        self._p_changed = 1
