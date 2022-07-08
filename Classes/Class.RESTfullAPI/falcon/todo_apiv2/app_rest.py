import falcon
import falcon_json_middleware
from falcon_rest.resources import ModelResource
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Base, Task, db_engine

class TaskSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Task

class TaskListResource(ModelResource):
    model = Task
    allowed_methods = ["GET", "POST"]
    serializer = TaskSerializer()

class TaskResource(ModelResource):
    model = Task
    allowed_methods = ["GET", "PATCH", "DELETE"]
    serializer = TaskSerializer()

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.media = {'result': 'Not found'}

api = falcon.API(middleware=[
            falcon_json_middleware.Middleware(),
      ])
api.add_sink(error_handle_404)
api.add_route('/todo/api/v2.0/tasks', TaskListResource(db_engine))
api.add_route('/todo/api/v2.0/tasks/{id}', TaskResource(db_engine))
