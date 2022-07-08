import falcon
import json
from tasks import tasks

class TaskListResource:
    def on_get(self, req, resp):
        resp.body = json.dumps(tasks)
    def on_post(self, req, resp):
        task = req.context['request']
        task['id'] = tasks[-1]['id'] + 1
        task['done'] = False
        tasks.append(task)
        resp.context['response'] = {'result': 'OK'}

class TaskResource:
    def on_get(self, req, resp, id):
        task_id = int(id)
        task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            resp.status = falcon.HTTP_404
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)
        else:
            resp.body = json.dumps(task[0])

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.body = 'Not found'

api = falcon.API()
api.add_sink(error_handle_404, '')
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
api.add_route('/todo/api/v1.0/tasks/{id}', TaskResource())
