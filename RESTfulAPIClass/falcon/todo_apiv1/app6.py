import falcon
from falcon import media
from tasks import tasks

def make_public_task(task, uri, id_included=False):
     new_task = task.copy()
     id = new_task.pop('id')
     if id_included:
        new_task['uri'] = uri
     else:
        new_task['uri'] = f'{uri}/{id}'
     return new_task

class TaskListResource:
    def on_get(self, req, resp):
        resp.media = {'tasks':
                      [make_public_task(task, req.uri) for task in tasks]
                     }
    def on_post(self, req, resp):
        task = req.media
        task['id'] = len(tasks) + 1
        task['done'] = False
        tasks.append(task)
        resp.media = {'result': 'OK'}

class TaskResource:
    def on_get(self, req, resp, id):
        id = int(id) -1
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            resp.status = falcon.HTTP_404
            resp.context['response'] = {'result': 'Not Found'}
        else:
            resp.media = {'tasks':
                           make_public_task(task, req.uri, id_included=True)

    def on_patch(self, req, resp, id):
        req_task = req.media
        id = int(id) -1
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            resp.status = falcon.HTTP_404
            resp.context['response'] = {'result': 'Not Found'}

        for key in ['title', 'description', 'done']:
            if key in req_task.keys():
                tasks[task_id][key] = req_task[key]
        resp.media = tasks[task_id]

    def on_delete(self, req, resp, id):
        id = int(id) -1
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            resp.status = falcon.HTTP_404
            resp.context['response'] = {'result': 'Not Found'}
        else:
            tasks.remove(tasks[0])
            resp.media = {'result': 'OK'}

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.media = {'result': 'Not found'}

api = falcon.API()
api.add_sink(error_handle_404)
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
api.add_route('/todo/api/v1.0/tasks/{id}', TaskResource())
