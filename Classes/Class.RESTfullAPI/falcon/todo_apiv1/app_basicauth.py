import falcon
from falcon import media
from tasks import tasks
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from authconfig import Allow_Users


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
        user = req.context['user']
        print(req.context)
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
        try:
            task_id = int(id) - 1
            task = tasks[task_id]
            resp.media = {'tasks':
                           make_public_task(task, req.uri, id_included=True)
                         }
        except IndexError:
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)
    def on_patch(self, req, resp, id):
        req_task = req.media
        task_id = int(id) - 1
        task = [task for task in tasks if task['id'] == task_id]
        if len(req_task) == 0:
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)
        for key in ['title', 'description', 'done']:
            if key in req_task.keys():
                tasks[task_id][key] = req_task[key]
        resp.media = {'tasks': tasks[task_id]}
    def on_delete(self, req, resp, id):
        try:
            task_id = int(id) - 1
            tasks.remove(tasks[task_id])
            resp.media = {'result': 'OK'}
        except IndexError:
            resp.context['response'] = {'result': 'Not Found'}
            raise falcon.HTTPError(falcon.HTTP_404)

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.media = {'result': 'Not found'}


def user_loader(username, password):
    print(f'Username={username}, Password={password}')
    if (username in Allow_Users.keys() and
        Allow_Users[username]['password'] == password):
        return username
    else:
        return None


auth_middleware = FalconAuthMiddleware(
                      BasicAuthBackend(user_loader),
                      exempt_routes=['/todo'],
                      exempt_methods=['HEAD'])

api = falcon.API(middleware=[auth_middleware])
api.add_sink(error_handle_404)
api.add_route('/todo/api/v1.0/tasks', TaskListResource())
api.add_route('/todo/api/v1.0/tasks/{id}', TaskResource())
