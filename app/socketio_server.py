from app import app, socketio
from app import db
from app.models import Reading

def ack():
    print('Message was received!')

@socketio.on('send_data')
def receive_data(json):

    temperature = json['temperature']
    humidity = json['humidity']
    timestamp = json['timestamp']

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