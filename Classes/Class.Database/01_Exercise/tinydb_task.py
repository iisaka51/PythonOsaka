from tinydb_base import DatabaseBase

class TaskDB(DatabaseBase):

    def __init__(self,
        file='tasks.json',
        table='tasks',
        requiredKeys='title:str,description:str,done:bool'):
        super().__init__(file=file,
                         table=table,
                         requiredKeys=requiredKeys)

        self.db = self.createObj().db
        self.tbl = self.createObj().tbl

    def _create_task(self, title='', descripton='', done=False):
        task = {'titile': title, 'decription': description, 'done': done}
        return task

    def add(self, title, description):
        return task_id

    def get(self, task_id=None):
        task = None
        return task

    def remove(self, task_id=None):
        return task_id

    def update(self, title, description, task_id=None):
        return task_id

    def done(self, task_id=None):
            pass
        return task_id

    def list(self):
        return self.tbl.all()

