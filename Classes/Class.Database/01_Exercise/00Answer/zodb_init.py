from zodb_task import *
from task_data import task_data
import transaction

db = TaskDB()

tasks = list()
for t in task_data:
    task = Task()
    task.setTask(t)
    db.tasks.append(task)

transaction.commit()
db.connection.close()
