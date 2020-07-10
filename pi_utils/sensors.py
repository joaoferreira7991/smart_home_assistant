import time
import board
import adafruit_dht
import RPi.GPIO
from datetime import datetime
import requests
import json
from json import JSONEncoder

DATA_PINS = {
    14 : board.D14,
    23 : board.D23
}

# URL to be ran
API_ENDPOINT = 'https://smart-home-assistant.herokuapp.com/update'

# Make security
# API_KEY

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

def dht11(data_pin):
    ''' 
    Function that initializes a dht11 sensor, and sends information every 60 seconds to the cloud.

    ...

    Parameters
    ----------
    data_pin : int 
        Number of the GPIO pin connected to the raspberry pi.
    '''
    dht11 = adafruit_dht.DHT11(DATA_PINS[data_pin])

    while True:
        try:
            # Gather the values
            temperature_c = float(dht11.temperature)
            humidity = dht11.humidity
            timestamp = datetime.now()

            print("T{}, H{}, D{}".format(temperature_c, humidity, timestamp))

            # Data to be sent to the API
            json_data = {
                "temperature" : temperature_c,
                "humidity" : humidity,
                "timestamp" : timestamp
            }
            request = requests.post(url=API_ENDPOINT, data=json.dumps(json_data, default=str))

        except RuntimeError as error:            
            pass

        # Read interval
        time.sleep(60.0)

#def apds_9002(data_pin):
#    ''' 
#    Function that initializes a apds_9002 sensor, and sends information every 60 seconds to the cloud.

#    ...

#    Parameters
#    ----------
#    data_pin : int 
#        Number of the GPIO pin connected to the raspberry pi.
#    '''

#    while True:
#        apds_9002 = APDS9002(DATA_PINS[data_pin])
#        print("{}".format(apds_9002.value()))


