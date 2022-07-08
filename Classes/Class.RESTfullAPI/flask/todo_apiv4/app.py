from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, reqparse, marshal
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), index = True)
    description = db.Column(db.Text(256))
    done = db.Column(db.Boolean)

    def __init__(self, title, description, done=False):
        self.title = title
        self.description = description
        self.done = done

    def __repr__(self):
        return f'Task: {self.title}'

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
    uri = ma.URLFor("task", id='<id>')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                   type = str, required = True,
                                   help = 'No task title provided',
                                   location = 'json')
        self.reqparse.add_argument('description',
                                   type = str, default = "",
                                   location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        args = self.reqparse.parse_args()
        task = Task(
                    title = args['title'],
                    description = args['description'],
               )
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task)

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                    type = str, location = 'json')
        self.reqparse.add_argument('description',
                                   type = str, location = 'json')
        self.reqparse.add_argument('done',
                                   type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        post = Task.query.get_or_404(id)
        return task_schema.dump(post)
    def put(self, id):
        args = self.reqparse.parse_args()
        task = Task.query.get_or_404(id)
        task.title = args['title']
        task.description = args['description']
        task.done = args['done']
        db.session.commit()
        return task_schema.dump(task)
    def delete(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204

api.add_resource(TaskListAPI,
                 '/todo/api/v4.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI,
                 '/todo/api/v4.0/tasks/<int:id>', endpoint = 'task')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task, 'TaskSchema': TaskSchema }


if __name__ == '__main__':
    app.run(port=8080)
