from falcon import API
import json
from tasks import tasks

class TaskListResource:
    def on_get(self, req, resp):
        resp.body = json.dumps(tasks)

class TaskResource:
    def on_get(self, req, resp, id):
        task_id = int(id) - 1
        resp.body = json.dumps(tasks[task_id])

api = API()
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
api.add_route('/todo/api/v1.0/tasks/{id}', TaskResource())
