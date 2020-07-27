from app import db, socketio
from app.models import Reading, data_type_dict
from flask_socketio import emit
from utils.json_util import DateTimeDecoder
import json

# Sensor reading
@socketio.on('send_data')
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

    emit('response', 'Message was received!')

# Led Strip Controller
@socketio.on('LED_ON')
def ledInit():
    emit('LED_ON')

@socketio.on('LED_OFF')
def ledStop():
    emit('LED_OFF')

@socketio.on('START_COLORSHIFT')
def colorshiftStart():
    emit('START_COLORSHIFT')

@socketio.on('INCREASE_BRIGHTNESS')
def brighnessIncrease():
    emit('INCREASE_BRIGHTNESS')

@socketio.on('DECREASE_BRIGHTNESS')
def brighnessDecrease():
    emit('DECREASE_BRIGHTNESS')