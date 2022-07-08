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
            print('Setup BTree into root.db')
            self.root.db = BTree()
        if 'tasks' not in self.root.db:
            print('initialized root.db')
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

    def add(self, title, description):
        task = Task()
        task = task.compose(title, description)
        self.tasks.append(task)
        task_id = len(self.tasks)
        transaction.commit()
        return task_id

    def get(self, task_id=None):
        try:
            self.tasks[task_id]
        except:
            pass
        return task_id

    def remove(self, task_id=None):
        try:
            self.tasks.remove[task_id]
        except:
            pass
        return task_id

    def update(self, title, description, done=False, task_id=None):
        try:
            self.tasks[task_id].title = title
            self.tasks[task_id].title = description
            self.tasks[task_id].done = done
        except:
            pass
        return task_id

    def done(self, task_id=None):
        try:
            self.tasks[task_id].done = True
        except:
            pass
        return task_id

    def list(self):
        return list(map(lambda x: x.getTask(), self.tasks))

