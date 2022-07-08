from task_data import task_data
from tinydb_task import *

db = TaskDB()

for t in task_data:
    db.tbl.insert(t)

db.tbl.all()

