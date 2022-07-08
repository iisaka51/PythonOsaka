import falcon
from falcon_autocrud.resource import CollectionResource, SingleResource
from falcon_autocrud.middleware import Middleware

from models import Base, Task, db_engine, TaskSchema

class TaskListResource(CollectionResource):
    model = Task

class TaskResource(SingleResource):
    model = Task

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.media = {'result': 'Not found'}

api = falcon.API(middleware=[
            Middleware(),
      ])
api.add_sink(error_handle_404)
api.add_route('/todo/api/v2.0/tasks', TaskListResource(db_engine))
api.add_route('/todo/api/v2.0/tasks/{id}', TaskResource(db_engine))
