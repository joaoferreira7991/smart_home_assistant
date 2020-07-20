from app import db, socketio
from app.models import Reading
from flask_socketio import emit
from utils.json_util import DateTimeDecoder
import json

def ack():
    print('Message was received!')

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

    emit('response', callback=ack)

@socketio.on('example')
def example():
    emit('example', 'ola cliente!')
    socketio.sleep(5)