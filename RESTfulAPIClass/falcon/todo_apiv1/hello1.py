from falcon import API
import json

class TaskListResource:
    def on_get(self, req, resp):
        greeting = {"greeting": "Hello World!" }
        resp.body = json.dumps(greeting)

api = API()
api.add_route('/greeting', TaskListResource())
