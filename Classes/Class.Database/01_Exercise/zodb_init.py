from zodb_task import *
from tasks import task_data
import transaction

db = TaskDB()

for t in task_data:
    task = Task()
    db.tasks.append(task)

transaction.commit()
db.connection.close()

