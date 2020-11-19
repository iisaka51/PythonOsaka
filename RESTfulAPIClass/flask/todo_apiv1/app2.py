from flask import Flask, jsonify, abort
from tasks import tasks

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasklist():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
