from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Database Related
# 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Signing Users Related
# 
login = LoginManager(app)
# Specify view that handles signing in
login.login_view = 'sign_in'

from app import routes, models, forms, errors
