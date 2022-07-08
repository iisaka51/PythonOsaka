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
        task = self._create_task(title, description)
        task_id = self.tbl.insert(task)
        return task_id

    def get(self, task_id=None):
        try:
            task = self.tbl.get(doc_id=task_id)
        except:
            task = None
        return task

    def remove(self, task_id=None):
        try:
            task_id = db.tbl.remove(doc_ids=[task_id])
        except:
            pass
        return task_id

    def update(self, title, description, task_id=None):
        task = self._create_task(title, description)
        try:
            task_id = self.tbl.update(task, doc_ids=[task_id])
        except:
            pass
        return task_id

    def done(self, task_id=None):
        try:
            task_id = self.tbl.update({'done': True}, doc_ids=[task_id])
        except:
            pass
        return task_id

    def list(self):
        return self.tbl.all()

