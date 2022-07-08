from falcon import API

class TaskListResource:
    def on_get(self, req, resp):
        resp.media = {"greeting": "Hello World!" }

api = API()
api.add_route('/greeting', TaskListResource())
