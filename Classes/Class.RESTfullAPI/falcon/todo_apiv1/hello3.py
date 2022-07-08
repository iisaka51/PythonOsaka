from falcon import API

class TaskListResource:
    def on_get(self, req, resp, name):
        resp.media = {"greeting": f"Hello {name}!" }

api = API()
api.add_route('/greeting/{name}', TaskListResource())
