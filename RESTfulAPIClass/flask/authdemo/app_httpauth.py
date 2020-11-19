from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import safe_str_cmp
from users import users, username_table


app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'),
                             password.encode('utf-8')):
        return user

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/')
@auth.login_required
def index():
    return {"Hello": "World"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
