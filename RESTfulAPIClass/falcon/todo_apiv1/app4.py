import falcon
import rapidjson as json
#import json
from tasks import tasks

class TaskListResource:
    def on_get(self, req, resp):
        resp.media = tasks
    def on_post(self, req, resp):
        task = req.media
        task['id'] = len(tasks) + 1
        task['done'] = False
        tasks.append(task)
        resp.media = {'result': 'OK'}

class TaskResource:
    def on_get(self, req, resp, id):
        def on_get(self, req, resp, id):
        id = int(id) -1
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)
        else:
            resp.body = json.dumps(tasks[task_id])

    def on_patch(self, req, resp, id):
        task = req.media
        task_id = int(id) - 1
        req_task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)
        for key in ['title', 'description', 'done']:
            if key in req_task.keys():
                tasks[key] = req_task[key]
        resp.media = tasks[task_id]

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.body = 'Not found'

api = falcon.API()
api.add_sink(error_handle_404, '')
api.req_options.auto_parse_form_urlencoded=True
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
api.add_route('/todo/api/v1.0/tasks/{id}', TaskResource())
