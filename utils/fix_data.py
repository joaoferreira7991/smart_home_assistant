from app.models import Reading, Actuator

# Transforms a Reading object into an array with (data_reading, timestamp).
def readingArr(arr : list()):
    aux = list()
    for i in arr:
        aux.append((i.data_reading, i.timestamp))
    return aux

# Transforms a Actuator object into an array with (id, name, state)
def actuatorArr(arr : list()):
    aux = list()
    for i in arr:
        aux.append((i.id, i.name, i.state_current))
    return aux

# Transforms a ControllerLed object into an array with (id, name, state_current, state_colorshift)
def controllerArr(arr : list()):
    aux = list()
    for i in arr:
        aux.append((i.id, i.name, i.state_current, i.state_colorshift))
    return aux