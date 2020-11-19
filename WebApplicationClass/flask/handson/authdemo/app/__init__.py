from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_login
from flask_debugtoolbar import DebugToolbarExtension
from flask_maintenance import Maintenance
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
toolbar = DebugToolbarExtension(app)
Maintenance(app)

from app import routes, models
