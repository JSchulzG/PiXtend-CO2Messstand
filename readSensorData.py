from pixtendv2l import PiXtendV2L
import serial
import time


class ReadSensorData():
    def __init__(self):
        self.p = PiXtendV2L()
        time.sleep(0.5)
        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 115200)
            if self.ser.is_open == False:
                self.ser.open()
        except:
            self.ser = None
        self.dummyPos = 22.0
        self.dummyDirection = 'right'

    def close(self):
        time.sleep(1)
        self.ser.close()
        self.p.close()

    def getTFminiData(self):
        count = self.ser.in_waiting
        if count > 8:
            recv = self.ser.read(9)
            self.ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:
                distance = recv[2] + recv[3]*256
                temp = recv[6] + recv[7]*256
                return (distance, temp)

    def distanceDummy(self):
        if self.dummyDirection == 'right':
            self.dummyPos += 0.02
        else:
            self.dummyPos -= 0.02
        if self.dummyPos >= 42:
            self.dummyDirection = 'left'
        if self.dummyPos <= 22.05:
            self.dummyDirection = 'right'
        return (self.dummyPos, 23.3)

    def heatLeftSide(self):
        self.p.digital_out0 = True
        self.p.digital_out1 = False

    def coldLeftSide(self):
        self.p.digital_out0 = False
        self.p.digital_out1 = True

    def heatRightSide(self):
        self.p.digital_out2 = True
        self.p.digital_out3 = False

    def coldRightSide(self):
        self.p.digital_out2 = False
        self.p.digital_out3 = True

    def read_Data(self):
        data = []
        scalling_T = 10.0
        """
        Wenn der Drucksensor auf einen Bereich von 1bar = 4mA und 100bar = 20mA eingestellt ist.
        """
        scalling_P = 15.625
        offset_P = -62.5
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
        '''
        try:
            distance, temp = self.getTFminiData()
        except:
            distance = 99
            temp = 9999
        '''
        distance, temp = self.distanceDummy()
        data.append(distance)
        data.append(temp)
        return data
