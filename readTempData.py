from pixtendv2l import PiXtendV2L
import serial
import time


class ReadTempData():
    def __init__(self):
        self.p = PiXtendV2L()
        self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        time.sleep(0.5)


    def close(self):
        time.sleep(1)
        self.ser.close()
        self.p.close()

    def getTFminiData(self):
        #self.ser.reset_input_buffer()
        #time.sleep(0.01)
        count = self.ser.in_waiting
        #print(count)
        if count > 8:
            recv = self.ser.read(9)
            #print(recv[0].encode('hex'))
            self.ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:
                #low = int(recv[2].encode('hex'), 16)
                #high = int(recv[3].encode('hex'), 16)
                distance = recv[2] + recv[3]*256
                temp = recv[6] + recv[7]*256
                #print('%i cm; %f °C' %(distance, temp))
                return (distance, temp)

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
        distance, temp = self.getTFminiData()
        data.append(distance)
        data.append(temp)
        return data
