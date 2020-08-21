from app.models import Reading, Actuator

# Transforms a Reading object into an array with (data_reading, timestamp).
def readingArr(arr : list()):
    aux = list()
    for i in arr:
        aux.append((i.data_reading, i.timestamp))
    return aux

# Transforms a Actuator object into an array with (id, name, state)
def actuatorArr_client(arr : list()):
    aux = list()
    for i in arr:
        aux.append({'id': i.id, 'name': i.name, 'state': i.state_current})
    return aux

# Transforms a ControllerLed object into an array with (id, name, state_current, state_colorshift)
def controllerArr_client(arr : list()):
    aux = list()
    for i in arr:
        aux.append({'id': i.id, 'name': i.name, 'state': i.state_current, 'colorshift': i.state_colorshift})
    return aux

# Transforms a Actuator object into an array with (id, ip, state)
def actuatorArr_pi(arr : list()):
    aux = list()
    for i in arr:
        aux.append({'id': i.id, 'ip': i.ip, 'state': i.state_current})
    return aux

# Transforms a ControllerLed object into an array with (id, name, state_current, state_colorshift)
def controllerArr_pi(arr : list()):
    aux = list()
    for i in arr:
        aux.append({'id': i.id, 'name': i.name, 'state': i.state_current, 'colorshift': i.state_colorshift})
    return aux