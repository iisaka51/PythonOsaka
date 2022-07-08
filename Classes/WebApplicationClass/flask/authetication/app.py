import flask
import flask_login
from forms import LoginForm

app = flask.Flask(__name__)
app.secret_key = 'K24rMLtDxlbW_PLoQQrAwg'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@app.route('/login')
def login():
    form = LoginForm()
    return flask.render_template('login.html', form=form)

