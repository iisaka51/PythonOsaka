import falcon
from falcon_sqla import Manager
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Base, Task, db_engine

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        ordered = True

class TaskBaseResource(object):
    model = Task
    schema = TaskSchema()
    def __init__(self, db):
        self.db = db
    def retrieve(self, req, resp, id=None):
        if id == None:
            raw_data = req.context.session.query(self.model).all()
            data = self.schema.dump(raw_data, many=True)
        else:
            raw_data = ( req.context.session.query(self.model)
                         .filter_by(id=id).first()
                       )
            data = self.schema.dump(raw_data)
        return data

    def add(self, req, resp):
        req_data = Task(title=req.media['title'],
                        description=req.media['description'])
        req.context.session.add(req_data)
        req.context.session.commit()
        data = self.schema.dump(req_data)
        return data

    def delete(self, req, resp, id=None):
        if id == None:
            raise falcon.HTTPBadRequest()
        else:
            raw_data = ( req.context.session.query(self.model)
                         .filter_by(id=id).first()
                       )
            if raw_data == None:
                data = None
            else:
                req.context.session.delete(raw_data)
                req.context.session.commit()
                data = self.schema.dump(raw_data)
        return data


    def patch(self, req, resp, id):
        raw_data = ( req.context.session.query(self.model)
                         .filter_by(id=id).first()
                    )
        if raw_data == None:
            data = None
        else:
            req_data = Task(title=req.media['title'],
                        description=req.media['description'])
            raw_data.title = req_data.title
            raw_data.description = req_data.description
            raw_data.done = req_data.done
            req.context.session.commit()
            data = self.schema.dump(raw_data)
        return data


class TaskListResource(TaskBaseResource):
    def on_get(self, req, resp):
        data = self.retrieve(req, resp)
        resp.media = {"data": data }
    def on_post(self, req, resp):
        data = self.add(req, resp)
        resp.media = {"data": data }


class TaskResource(TaskBaseResource):
    def on_get(self, req, resp, id):
        try:
            data = self.retrieve(req, resp, id)
            resp.media = {"data": data }
        except IndexError:
            resp.status = falcon.HTTP_404
            resp.media = {'result': 'Not Found'}
    def on_delete(self, req, resp, id):
        result = self.delete(req, resp, id)
        if result != None:
            resp.media = {'result': 'OK'}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {'result': 'Not Found'}
    def on_patch(self, req, resp, id):
        result = self.patch(req, resp, id)
        if result != None:
            resp.media = {'result': 'OK'}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {'result': 'Not Found'}

def error_handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.media = {'result': 'Not found'}

api = falcon.API(middleware=[
            Manager(db_engine).middleware,
      ])
api.add_sink(error_handle_404)
api.add_route('/todo/api/v2.0/tasks', TaskListResource(db_engine))
api.add_route('/todo/api/v2.0/tasks/{id}', TaskResource(db_engine))
