import time
import board
import adafruit_dht
from datetime import datetime
import requests

DATA_PINS = {
    14 : board.D14
}

# URL to be ran
API_ENDPOINT = 'https://smart-home-assistant.herokuapp.com/update'

# Make security
# API_KEY

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
                'temperature' : temperature_c,
                'humidity' : humidity,
                'timestamp' : timestamp
            }

            request = requests.post(url=API_ENDPOINT, data=json_data)

        except RuntimeError as error:            
            pass

        # Read interval
        time.sleep(60.0)

#def loadSensors():

