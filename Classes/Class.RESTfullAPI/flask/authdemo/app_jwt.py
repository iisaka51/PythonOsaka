from flask import Flask, jsonify, make_response
from flask_jwt import JWT, jwt_required
from werkzeug.security import safe_str_cmp
from users import users, username_table, userid_table

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'),
                             password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.config['SECRET_KEY'] = '2904c118551f558ba71085d0555bc2fead56d5fe508e3fa3'
jwt = JWT(app, authenticate, identity)

@app.route('/')
@jwt_required()
def index():
    return {"Hello": "World"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
