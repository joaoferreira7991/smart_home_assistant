from app import db, socketio
from app.models import Reading, data_type_dict, Actuator, ControllerLed
from app.forms import ActuatorCreateForm, ControllerCreateForm
from flask_socketio import emit
from utils.json_util import DateTimeDecoder, DateTimeEncoder
from utils.fix_data import readingArr, actuatorArr_client, actuatorArr_pi, controllerArr_client, controllerArr_pi, controller_pi
from datetime import datetime, time, date, timedelta
from werkzeug.datastructures import MultiDict
import json, sys


# ---------------------------------------
# Namespace '/client-user' related events
# Connect event
@socketio.on('connect', namespace='/client-user')
def connect_user():
    loadActuator()
    loadData()

# Form events
@socketio.on('submitForm', namespace='/client-user')
def submitForm(data):
    print(data)
    if data['type'] == 'actuator':
        print('actuator')
        data.pop('type')
        print(data)
        form = ActuatorCreateForm(MultiDict(data))
        if form.validate():
            print('validate')
            oActuator = Actuator(name=form.name.data, ip=form.ip.data)
            db.session.add(oActuator)
            db.session.commit()            
            loadActuator()
            return {
                'OK' : 1
            } 
        else :            
            return json.dumps(form.errors)

    elif data['type'] == 'controller':
        print('controller')
        data.pop('type')
        print(data)
        form = ControllerCreateForm(MultiDict(data))
        if form.validate():
            print('validate')
            oController = ControllerLed(name=form.name.data, gpio_red=form.red.data, gpio_green=form.green.data, gpio_blue=form.blue.data)
            db.session.add(oController)
            db.session.commit()
            loadActuator()
            socketio.emit('addController', data=controller_pi(oController), namespace='/client-pi')
            return {
                'OK' : 1
            } 
        else :            
            return json.dumps(form.errors)

# Database reading events
@socketio.on('loadData', namespace='/client-user')
def loadData(background=0, date_range=datetime.today(), max_results=120):
    while True:
        # Fix date_range to correctly show today without time values
        date_range = date_range.replace(hour=0, minute=0, second=0,microsecond=0)
        
        # Query the database
        latestTemp = Reading.query.filter_by(data_type=data_type_dict['dht11_temperature']).order_by(Reading.id.desc()).first()
        latestHum = Reading.query.filter_by(data_type=data_type_dict['dht11_humidity']).order_by(Reading.id.desc()).first()
        aTemperature = Reading.query.filter(Reading.data_type==data_type_dict['dht11_temperature'], Reading.timestamp > date_range).order_by(Reading.timestamp.desc()).limit(max_results).all()
        aHumidity = Reading.query.filter(Reading.data_type==data_type_dict['dht11_humidity'], Reading.timestamp > date_range).order_by(Reading.timestamp.desc()).limit(max_results).all()
        
        # Transform data to be sent
        arrTemperature = readingArr(aTemperature)
        arrHumidity = readingArr(aHumidity)
        
        data =   {  'latest_temp'       :   latestTemp.data_reading,
                    'latest_hum'        :   latestHum.data_reading,
                    'temp_arr'          :   arrTemperature,
                    'hum_arr'           :   arrHumidity}
        socketio.emit('loadData', data=json.dumps(data, cls=DateTimeEncoder), namespace='/client-user')
        if background == 0:
            break
        socketio.sleep(60)

@socketio.on('loadActuator', namespace='/client-user')
def loadActuator():
    # Query the database
    aController = ControllerLed.query.all() 
    aActuator = Actuator.query.all()

    # Transform data to be sent
    arrController = controllerArr_client(aController)
    arrActuator = actuatorArr_client(aActuator)

    data =  {
        'controller_arr'    :   arrController,
        'actuator_arr'      :   arrActuator}
    socketio.emit('loadActuator', data=json.dumps(data), namespace='/client-user')

# Actuator handling events
@socketio.on('switchClick', namespace='/client-user')
def switchClick(data):
    oActuator = Actuator.query.filter_by(id=data['id']).first()
    if oActuator is not None:
        data = {
            'id' : oActuator.id,
            'ip' : oActuator.ip,
            'state' : oActuator.state_current
        }
        if oActuator.state_current:
            socketio.emit('switchOff', data=data, namespace='/client-pi', callback=switchClick_ack)
        elif not oActuator.state_current:
            socketio.emit('switchOn', data=data, namespace='/client-pi', callback=switchClick_ack)            

# Callback function that updates data from the actuator and then emits a visual update to all clients connected.
def switchClick_ack(data=None):

    # if the callback is called with no data then just pass
    if data is None:
        return

    parsed = json.loads(data)
    oActuator = Actuator.query.filter_by(id=parsed['id']).first()
    if oActuator is not None:
        # Update database
        oActuator.state_current = parsed['state']       
        db.session.commit()
        # Update client-user's button state
        aux = {
            'id' : parsed['id'],
            'state' : parsed['state'],
            'class' : 'switch-onoff'
        }
        socketio.emit('updateState', data=aux, namespace='/client-user')

@socketio.on('switchDel', namespace='/client-user')
def switchDel(data):
    oActuator = Actuator.query.filter_by(id=data['id']).first()
    if oActuator is not None:
        # Delete row
        db.session.delete(oActuator)
        db.session.commit()
        socketio.emit('deleteActuator', data=data, namespace='/client-user')

# Led Strip Controller events
@socketio.on('ledClick', namespace='/client-user')
def ledClick(data):
    oControllerLed = ControllerLed.query.filter_by(id=data['id']).first()
    if oControllerLed is not None:
        aux = controller_pi(oControllerLed)
        if oControllerLed.state_current:
            socketio.emit('ledOff', data=aux, namespace='/client-pi', callback=ledClick_ack)
        if not oControllerLed.state_current:
            socketio.emit('ledOn', data=aux, namespace='/client-pi', callback=ledClick_ack)

def ledClick_ack(data=None):

    # if the callback is called with no data then just pass
    if data is None:
        return

    parsed = json.loads(data)
    oControllerLed = ControllerLed.query.filter_by(id=parsed['id']).first()
    if oControllerLed is not None:
        # Update database
        oControllerLed.state_current = parsed['state']
        db.session.commit()
        # Update client-user's button state
        aux = {
            'id' : parsed['id'],
            'state' : parsed['state'],
            'state_colorshift' : oControllerLed.state_colorshift,
            'class' : 'controller-onoff'
        }
        socketio.emit('updateState', data=aux, namespace='/client-user')


@socketio.on('colorshiftClick', namespace='/client-user')
def colorshiftClick(data):
    oControllerLed = ControllerLed.query.filter_by(id=data['id']).first()
    if oControllerLed is not None:
        aux = controller_pi(oControllerLed)
        if oControllerLed.state_colorshift:
            socketio.emit('stopColorshift', data=aux, namespace='/client-pi', callback=colorshiftClick_ack)
        if not oControllerLed.state_colorshift:
            socketio.emit('startColorshift', data=aux, namespace='/client-pi', callback=colorshiftClick_ack)        

def colorshiftClick_ack(data=None):

    # if the callback is called with no data then just pass
    if data is None:
        return

    parsed = json.loads(data)
    oControllerLed = ControllerLed.query.filter_by(id=parsed['id']).first()
    if oControllerLed is not None:
        # Update database
        oControllerLed.state_colorshift = parsed['state_colorshift']
        if not parsed['state_colorshift']:
            oControllerLed.state_red = parsed['red']
            oControllerLed.state_green = parsed['green']
            oControllerLed.state_blue = parsed['blue']
        db.session.commit()
        # Update client-user's button state
        aux = {
            'id' : parsed['id'],
            'state' : parsed['state_colorshift'],
            'class' : 'controller-colorshift'
        }
        socketio.emit('updateState', data=aux, namespace='/client-user')

@socketio.on('increaseBrightness', namespace='/client-user')
def increaseBrightness(data):
    oControllerLed = ControllerLed.query.filter_by(id=data['id']).first()
    if oControllerLed is not None:
        aux = controller_pi(oControllerLed)
        socketio.emit('increaseBrightness', data=aux, namespace='/client-pi', callback=brightness_ack)

@socketio.on('decreaseBrightness', namespace='/client-user')
def decreaseBrightness(data):
    oControllerLed = ControllerLed.query.filter_by(id=data['id']).first()
    if oControllerLed is not None:
        aux = controller_pi(oControllerLed)
        socketio.emit('decreaseBrightness', data=aux, namespace='/client-pi', callback=brightness_ack)

def brightness_ack(data=None):

    # if the callback is called with no data then just pass
    if data is None:
        return

    parsed = json.loads(data)
    oControllerLed = ControllerLed.query.filter_by(id=parsed['id']).first()
    if oControllerLed is not None:
        # Update database
        oControllerLed.state_brightness = parsed['brightness']
        db.session.commit()

@socketio.on('controllerDel', namespace='/client-user')
def controllerDel(data):
    oControllerLed = ControllerLed.query.filter_by(id=data['id']).first()
    if oControllerLed is not None:
        # Delete row
        db.session.delete(oControllerLed)
        db.session.commit()
        socketio.emit('deleteController', data=controller_pi(oControllerLed), namespace='/client-pi')
        socketio.emit('deleteController', data=data, namespace='/client-user')

# -------------------------------------
# Namespace '/client-pi' related events
# Connect event
# Sends last recorded state of the actuators and led_controllers in the database
@socketio.on('connect', namespace='/client-pi')
def connect_pi():
    aActuator = Actuator.query.all()
    aControllerLed = ControllerLed.query.all()
    arrActuator = actuatorArr_pi(aActuator)
    arrControllerLed = controllerArr_pi(aControllerLed)
    data = {
        'arrActuator' : arrActuator,
        'arrControllerLed' : arrControllerLed
    }
    socketio.emit('loadData', json.dumps(data), namespace='/client-pi')

# Background task to emit a request for sensor data to the gateway pi every 60 seconds
def sendData():
    while True:
        socketio.emit('sendData', namespace='/client-pi')
        socketio.sleep(60)

# Receives event with sensor data
@socketio.on('receiveData', namespace='/client-pi')
def receiveData(json_data):
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
    return 'Message was received!'

socketio.start_background_task(loadData, '1')
socketio.start_background_task(sendData)