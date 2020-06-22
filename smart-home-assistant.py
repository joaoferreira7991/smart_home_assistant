from app import app, db
from app.models import User, Home, Sensor, Actuator, Reading

@app.shell_context_processor
def make_shell_context():
    return {
        'db':db, 
        'User':User,
        'Home':Home,
        'Sensor':Sensor,
        'Actuator':Actuator,
        'Reading':Reading,
        }
