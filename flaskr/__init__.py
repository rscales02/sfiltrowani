from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# create and configure an instance of class Flask
app = Flask(__name__)
app.config.from_object(Config)
# create user database
db = SQLAlchemy(app)
# implement ability to make changes to database
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from flaskr import routes, models
