from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

# Flask App
app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

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

if __name__ == "__main__":
    socketio.run(app)
