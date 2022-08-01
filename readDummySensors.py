import time
import random

class ReadSensorData():
    def __init__(self):
        time.sleep(0.5)



    def close(self):
        time.sleep(1)

    def _getRandomFloat(self):
        return random.randint(0,1000)/10

    def read_Data(self):
        data = []
        for i in range(6):
            data.append(self._getRandomFloat())
        data.append(random.randint(17, 41))
        data.append(2405)
        #print(data)
        return data
