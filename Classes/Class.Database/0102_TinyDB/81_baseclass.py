from tinydb_base import DatabaseBase

class Task(DatabaseBase):

    def __init__(self,
        file: str ='tasks.json',
        table: str ='tasks',
        requiredKeys: str ='title:str,item:str,quantity:int'):
        super().__init__(file=file,
                         table=table,
                         requiredKeys=requiredKeys)

task = Task()
task.create({'title': 'Buy Beer', 'item': 'Badweiser', 'quantity':1})

# task.readAll()
