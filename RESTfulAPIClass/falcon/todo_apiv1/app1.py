from falcon import API
import json
from tasks import tasks

class TaskListResource:
    def on_get(self, req, resp):
        resp.body = json.dumps(tasks)

api = API()
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
