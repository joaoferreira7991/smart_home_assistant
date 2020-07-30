from app import db, socketio
from app.models import Reading, data_type_dict
from flask_socketio import emit
from utils.json_util import DateTimeDecoder
import json

@socketio.on('connect', namespace='/client-pi')
def connect_pi():
    emit('response', 'Raspberry Pi is connected.', namespace='/client-pi')

@socketio.on('connect', namespace='/client-user')
def connect_user():
    print('Ola')

# Sensor reading
@socketio.on('send_data', namespace='/client-pi')
def receive_data(json_data):
    aux = json.loads(json_data, cls=DateTimeDecoder)
    temperature = aux['temperature']
    humidity = aux['humidity']
    timestamp = aux['timestamp']

    temperature_reading = Reading(timestamp, temperature, data_type_dict['dht11_temperature'])
    humidity_reading = Reading(timestamp, humidity, data_type_dict['dht11_humidity'])
    db.session.add(temperature_reading)
    db.session.commit()
    db.session.add(humidity_reading)
    db.session.commit()

    emit('response', 'Message was received!', namespace='/client-pi')

# Led Strip Controller
@socketio.on('LED_ON', namespace='/client-user')
def ledInit():
    socketio.emit('LED_ON', namespace='/client-pi')

@socketio.on('LED_OFF', namespace='/client-user')
def ledStop():
    emit('LED_OFF', namespace='/client-pi')

@socketio.on('START_COLORSHIFT', namespace='/client-user')
def colorshiftStart():
    emit('START_COLORSHIFT', namespace='/client-pi')

@socketio.on('INCREASE_BRIGHTNESS', namespace='/client-user')
def brighnessIncrease():
    emit('INCREASE_BRIGHTNESS', namespace='/client-pi')

@socketio.on('DECREASE_BRIGHTNESS', namespace='/client-user')
def brighnessDecrease():
    emit('DECREASE_BRIGHTNESS', namespace='/client-pi')