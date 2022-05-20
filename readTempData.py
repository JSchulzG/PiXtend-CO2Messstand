from pixtendv2l import PiXtendV2L
import time


class ReadTempData():
    def __init__(self):
        self.p = PiXtendV2L()
        time.sleep(0.5)


    def close(self):
        time.sleep(1)
        self.p.close()
        

    def read_Data(self):
        data = []
        scalling_T = 10.0
        """
        Wenn der Drucksensor auf einen Bereich von 1bar = 4mA und 100bar = 20mA eingestellt ist.
        """
        scalling_P = 6.1875
        offset_P = -23.75
        raw_Data = self.p.analog_in0
        data.append(raw_Data*scalling_T)
        raw_Data = self.p.analog_in1
        data.append(raw_Data*scalling_T)
        raw_Data = self.p.analog_in2
        data.append(raw_Data*scalling_T)
        raw_Data = self.p.analog_in3
        data.append(raw_Data*scalling_T)
        raw_Data = self.p.analog_in4
        data.append(raw_Data*scalling_P + offset_P)
        raw_Data = self.p.analog_in5
        data.append(raw_Data*scalling_P + offset_P)
        return data
