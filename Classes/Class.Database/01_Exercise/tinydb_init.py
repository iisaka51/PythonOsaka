from task_model import *
from tasks import task_data

task = Task()
db = task.createObj()

for t in task_data:
    db.tbl.insert(t)

db.tbl.all()

