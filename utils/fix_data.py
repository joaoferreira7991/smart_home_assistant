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