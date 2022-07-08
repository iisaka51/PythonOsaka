import ZODB
from persistent import Persistent
from BTrees.OOBTree import BTree
import transaction

class Task(Persistent):
    def setTask(self, task):
        self.task = task
    def getTask(self):
        return self.task
    def compose(self, title='', description='', done=False):
        task = {'titile': title, 'decription': description, 'done': done}
        self.task = task

class TaskDB():
    def __init__(self, file='tasks.fs'):
        self.open(file)
        self.root = self.connection.root
        if 'db' not in self.root._root:
            print('setup BTree()')
            self.root.db = BTree()
        if 'tasks' not in self.root.db:
            print('setup list()')
            self.root.db['tasks'] = list()
        self.tasks = self.root.db['tasks']

    def commit(self):
        return transaction.commit()

    def open(self, file):
        self.db = ZODB.DB(file)
        self.connection = self.db.open()
        return self.connection

    def close(self):
        return self.connection.close()

    def add(self):
        pass

    def get(self):
        pass

    def remove(self):
        pass

    def update(self):
        pass

    def done(self):
        pass

    def list(self):
        print(self.tasks)
        return list(map(lambda x: x.getTask(), self.tasks))

