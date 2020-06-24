from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Home(db.Model):
    # To make naming houses more flexible we could implement a naming
    # scheme like this 'myHouse#123' where 'myHouse' is the name
    # and 123 is the id of the house. 'myHouse#123' could be a tag,
    # that would be unique for each house. 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    # Creation of a one-to-one relashionship between Home and User
    user = db.relationship('User', backref='user', lazy=True, uselist=False)
    # Creation of a one-to-many relationship between Home and (Sensor/Actuator)
    sensors = db.relationship('Sensor', backref='sensors', lazy=True)
    actuators = db.relationship('Actuator', backref='actuators', lazy=True)
    # Could add more info

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Home {}>'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    # Unsure of password optimal length
    password = db.Column(db.String(512), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=True)
    # Might add more information, such as full name not unique and more

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)
    
    # Returns true if the password is correct or false if it's incorrect
    def check_password(self, password):    
        return check_password_hash(self.password, password)

    # home_id is supposed to be set as null initially, then it will be created and assigned.
    def set_home_id(home_id):
        self.home_id = home_id

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

    def set_home_id(home_id):
        self.home_id = home_id

class Actuator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    interruptor = db.Column(db.Boolean, nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        self.interruptor = False

    def __repr__(self):
        return '<Actuator {}>'.format(self.name)

    def set_home_id(home_id):
        self.home_id = home_id


# Dictionary meant for assigning data_type string to an integer value, 
#   to be inserted in the database instead.
data_type_dict = {
    'dht11_temperature' : 0,
    'dht11_humidity' : 1,
    '_luminance' : 2
}

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now, nullable=False)
    data_reading = db.Column(db.Float, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    #sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)

    def __init__(self, timestamp, data_reading, data_type):
        self.timestamp = timestamp
        self.data_reading = data_reading
        self.data_type = data_type
    
    def __repr__(self):
        return '<Reading {}>'.format(self.id, self.data_reading)
    
    #def set_sensor_id(sensor_id):
    #    self.sensor_id = sensor_id

