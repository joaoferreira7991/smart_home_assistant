from app import db, socketio
from app.models import Reading, data_type_dict
from flask_socketio import emit
from utils.json_util import DateTimeDecoder
import json

# ---------------------------------------
# Namespace '/client-user' related events
# Connect event
@socketio.on('connect', namespace='/client-user')
def connect_user():
    print('Ola')

# Database reading events
@socketio.on('updateTemp', namespace='/client-user')
def updateTemp():
    while True:
        latestTemp = Reading.query.filter_by(data_type=data_type_dict['dht11_temperature']).order_by(Reading.id.desc()).first()
        socketio.emit('updateTemp', data=latestTemp, namespace='/client-user')
        socketio.sleep(60)

# Actuator handling events
# Led Strip Controller events
@socketio.on('LED_ON', namespace='/client-user')
def ledInit():
    socketio.emit('LED_ON', namespace='/client-pi')

@socketio.on('LED_OFF', namespace='/client-user')
def ledStop():
    socketio.emit('LED_OFF', namespace='/client-pi')

@socketio.on('START_COLORSHIFT', namespace='/client-user')
def colorshiftStart():
    socketio.emit('START_COLORSHIFT', namespace='/client-pi')

@socketio.on('INCREASE_BRIGHTNESS', namespace='/client-user')
def brighnessIncrease():
    socketio.emit('INCREASE_BRIGHTNESS', namespace='/client-pi')

@socketio.on('DECREASE_BRIGHTNESS', namespace='/client-user')
def brighnessDecrease():
    socketio.emit('DECREASE_BRIGHTNESS', namespace='/client-pi')

# -------------------------------------
# Namespace '/client-pi' related events
# Connect event
@socketio.on('connect', namespace='/client-pi')
def connect_pi():
    emit('response', 'Raspberry Pi is connected.', namespace='/client-pi')

# Sensor handling events
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

# Start background tasks
# socketio.start_background_task(updateTemp)