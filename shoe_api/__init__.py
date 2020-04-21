from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask Login Manager Import
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_info = LoginManager(app)
login_info.login_view = 'login'

from shoe_api import models,routes