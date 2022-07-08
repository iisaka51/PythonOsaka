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

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flask.flash(f'Login requested for user {form.username.data}')
        return flask.redirect('/index')
    return flask.render_template('login2.html', title='Sign In', form=form)

@app.route('/index')
def index():
    return 'index'
