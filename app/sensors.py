import time
import board
import adafruit_dht
from datetime import datetime
from app.models import Sensor, Reading
from app import db

DATA_PINS = {
    14 : board.D14
}


def dht11(sensor_id, data_pin):
    ''' 
    Function that initializes a dht11 sensor, and retrieves information every 60 seconds to the database,
    based on the given id.

    ...

    Parameters
    ----------
    sensor_id : int 
        Id of the sensor in database.
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

            # Check sensor_id if exists in database
            id = Sensor.query.filter_by(id=sensor_id).first()
            if id is None:
                print("No id given.")        
            else :
                read = Reading(timestamp, temperature_c)
                read.sensor_id = id
                db.session.add(read)
                db.session.commit()

            

        except RuntimeError as error:
            # print("error")
            pass

        # Read interval
        time.sleep(5.0)

#def loadSensors():

