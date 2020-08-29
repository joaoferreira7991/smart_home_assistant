from app.models import Reading, Actuator, ControllerLed

# Client transforming functions
# -----------------------------

# Transforms a Reading object into into a dictionary array.
def readingArr(arr: list()):
    aux = list()
    for i in arr:
        aux.append((i.data_reading, i.timestamp))
    return aux

# Transforms a Actuator object into into a dictionary array.
def actuatorArr_client(arr: list()):
    aux = list()
    for i in arr:
        aux.append({
            'id': i.id,
            'name': i.name,
            'state': i.state_current
        })
    return aux

# Transforms a ControllerLed object into into a dictionary array.
def controllerArr_client(arr: list()):
    aux = list()
    for i in arr:
        aux.append({
            'id': i.id, 
            'name': i.name, 
            'state': i.state_current, 
            'state_colorshift': i.state_colorshift
        })
    return aux

# Gateway pi transforming functions
# ---------------------------------

# Transforms a Actuator object array into into a dictionary array.
def actuatorArr_pi(arr: list()):
    aux = list()
    for i in arr:
        aux.append({
            'id': i.id, 
            'ip': i.ip, 
            'state': i.state_current
        })
    return aux

# Transforms a ControllerLed object array into a dictionary array.
def controllerArr_pi(arr: list()):
    aux = list()
    for i in arr:
        aux.append({
            'id' : i.id,
            'red' : i.state_red,
            'green' : i.state_blue,
            'blue' : i.state_green,
            'state': i.state_current,
            'state_colorshift' : i.state_colorshift,
            'brightness' : i.state_brightness,
            'gpio_red' : i.gpio_red,
            'gpio_green' : i.gpio_green,
            'gpio_blue' : i.gpio_blue
        })
    return aux

# Transforms a ControllerLed object into a dictionary.
def controller_pi(o: ControllerLed):
    return {
        'id' : o.id,
        'red' : o.state_red,
        'green' : o.state_blue,
        'blue' : o.state_green,
        'state' : o.state_current,
        'state_colorshift' : o.state_colorshift,
        'brightness' : o.state_brightness,
        'gpio_red' : o.gpio_red,
        'gpio_green' : o.gpio_green,
        'gpio_blue' : o.gpio_blue
    }
    