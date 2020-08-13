from app import db, socketio
from app.models import Reading, data_type_dict, Actuator, ControllerLed
from flask_socketio import emit
from utils.json_util import DateTimeDecoder, DateTimeEncoder
from utils.fix_data import readingArr, actuatorArr
from datetime import datetime, time, date, timedelta
import json, sys


# ---------------------------------------
# Namespace '/client-user' related events
# Connect event

# Database reading events
@socketio.on('loadData', namespace='/client-user')
def loadData(background=0, date_range=datetime.today(), max_results=30):
    while True:
        # Query the database
        #latestTemp = Reading.query.filter_by(data_type=data_type_dict['dht11_temperature']).order_by(Reading.id.desc()).first()
        #latestHum = Reading.query.filter_by(data_type=data_type_dict['dht11_humidity']).order_by(Reading.id.desc()).first()
        aController = ControllerLed.query.all() 
        aActuator = Actuator.query.all()
        aTemperature = Reading.query.filter(Reading.data_type==data_type_dict['dht11_temperature'], Reading.timestamp > date_range).order_by(Reading.id.asc()).limit(max_results).all()
        aHumidity = Reading.query.filter(Reading.data_type==data_type_dict['dht11_humidity'], Reading.timestamp > date_range).order_by(Reading.id.asc()).limit(max_results).all()
        
        # Transform data to be sent
        arrController = controllerArr(aController)
        arrActuator = actuatorArr(aActuator)
        arrTemperature = readingArr(aTemperature)
        arrHumidity = readingArr(aHumidity)
        
        data =   {  'controller_arr'    :   arrController,
                    'actuator_arr'      :   arrActuator,
                    'temp_arr'          :   arrTemperature,
                    'hum_arr'           :   arrHumidity}
        socketio.emit('loadData', data=json.dumps(data, cls=DateTimeEncoder), namespace='/client-user')
        if background == 0:
            break
        socketio.sleep(60)

# Actuator handling events
# Led Strip Controller events
@socketio.on('LED_ON', namespace='/client-user')
def ledInit():
    print('init')
    socketio.emit('LED_ON', namespace='/client-pi')

@socketio.on('LED_OFF', namespace='/client-user')
def ledStop():
    print('stop')
    socketio.emit('LED_OFF', namespace='/client-pi')

@socketio.on('START_COLORSHIFT', namespace='/client-user')
def colorshiftStart():
    socketio.emit('START_COLORSHIFT', namespace='/client-pi')
    
@socketio.on('STOP_COLORSHIFT', namespace='/client-user')
def colorshiftStop():
    socketio.emit('STOP_COLORSHIFT', namespace='/client-pi')

@socketio.on('INCREASE_BRIGHTNESS', namespace='/client-user')
def brighnessIncrease():
    socketio.emit('INCREASE_BRIGHTNESS', namespace='/client-pi')

@socketio.on('DECREASE_BRIGHTNESS', namespace='/client-user')
def brighnessDecrease():
    socketio.emit('DECREASE_BRIGHTNESS', namespace='/client-pi')

# -------------------------------------
# Namespace '/client-pi' related events
# Connect event
# Sends last recorded state of the actuators in the database
@socketio.on('connect', namespace='/client-pi')
def connect_pi():
    arrActuator = Actuator.query.all()
    arrControllerLed = ControllerLed.query.all()
    data = {'arrActuator' : arrActuator,
            'arrControllerLed' : arrControllerLed}
    emit('loadData', json.dumps(data), namespace='/client-pi')

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

socketio.start_background_task(loadData, '1')