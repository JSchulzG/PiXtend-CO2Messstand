from pixtendv2l import PiXtendV2L
import time


class ReadTempData():
    def __init__(self):
        self.p = PiXtendV2L()
        time.sleep(0.5)
        #self.p.analog_out0 = 1023
        time.sleep(0.5)
        #self.p.analog_out1 = 508

    def close(self):
        #self.p.analog_out1 = 0
        #self.p.analog_out0 = 0
        time.sleep(1)
        self.p.close()
        

    def read_Data(self):
        data = []
        scalling = 10.0
        raw_Data = self.p.analog_in0
        data.append(raw_Data*scalling)
        raw_Data = self.p.analog_in1
        data.append(raw_Data*scalling)
        raw_Data = self.p.analog_in2
        data.append(raw_Data*scalling)
        raw_Data = self.p.analog_in3
        data.append(raw_Data*scalling)
        return data
