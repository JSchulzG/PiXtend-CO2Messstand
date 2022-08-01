# This Python file uses the following encoding: utf-8
import time
import os
from pathlib import Path
import pandas as pd
import sys

#import readSensorData
import readDummySensors as rSD

import numpy as np


from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer




class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = self.load_ui()
        self.writeList = [self.writeT1, self.writeT2, self.writeT3, self.writeT4, self.writeP1, self.writeP1, self.writeP2]
        for i in self.writeList:
            i.setVisible(False)
        self.checkSaveList = [self.checkSaveT1, self.checkSaveT2, self.checkSaveT3, self.checkSaveT4, self.checkSaveP1, self.checkSaveP2]

        self.sliderPosition.setMinimum(1)
        self.sliderPosition.setMaximum(17)

        self.valueT1.setText('%.1f °C' % 0)
        self.valueT2.setText('%.1f °C' % 0)
        self.valueT3.setText('%.1f °C' % 0)
        self.valueT4.setText('%.1f °C' % 0)
        self.sensorList = [self.valueT1, self.valueT2, self.valueT3, self.valueT4, self.valueP1, self.valueP2]
        #self.step = 0
        #self.step_plot = 0
        self.value = 0.0
        self.saving = None
        self.data = {}
        self.qTimer = QTimer()
        self.qTimer.setInterval(50)  # 50ms max PiXtend is not as fast :(
        self.qTimer.timeout.connect(self.getSensorData)
        self.qTimer.start()
        self.saveBtn.clicked.connect(self.writeData)
        self.stopBtn.clicked.connect(self.stopExit)
        #self.canvas = MplCanvas(self)
        #l = QVBoxLayout(self.plot2Widget)
        #l.addWidget(self.canvas)
        #self.sensors = readSensorData.ReadSensorData()
        self.sensors = rSD.ReadSensorData()

    def load_ui(self):
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        loadUi(path, self)

    def getSensorData(self):
        #self.value = self.dummiSensor.getData()
        self.value = self.sensors.read_Data()
        for i in range(6):
            if i < 4:
                self.sensorList[i].setText('%.1f °C' % self.value[i])
            else:
                self.sensorList[i].setText('%.1f Bar' % self.value[i])
        position = 42 - self.value[6]
        self.sliderPosition.setValue(position)
        self.valuePosition.setText("%i cm" % position)
        self.valueTOut.setText("%.1f °C" % (self.value[7]/100))
        if self.saving is True:
            _now = time.time()
            t = time.strftime('%X', time.localtime(_now)) + '.' + str('%.3f' % _now).split('.')[1]
            self.data['Time'].append(t)
            if self.checkSaveT1.isChecked() is True:
                self.data['T1/[°C]'].append(self.valueT1.text().split(' ')[0])
            if self.checkSaveT2.isChecked() is True:
                self.data['T2/[°C]'].append(self.valueT2.text().split(' ')[0])
            if self.checkSaveT3.isChecked() is True:
                self.data['T3/[°C]'].append(self.valueT3.text().split(' ')[0])
            if self.checkSaveT4.isChecked() is True:
                self.data['T4/[°C]'].append(self.valueT4.text().split(' ')[0])
            if self.checkSaveP1.isChecked() is True:
                self.data['P1/[Bar]'].append(self.valueP1.text().split(' ')[0])
            if self.checkSaveP2.isChecked() is True:
                self.data['P2/[Bar]'].append(self.valueP2.text().split(' ')[0])
            self.data['Pos/[cm]'].append(self.valuePosition.text().split(' ')[0])
            self.data['TOut/[°C]'].append(self.valueTOut.text().split(' ')[0])


    def writeData(self):
        if self.saving is False or self.saving is None:
            self.saving = True
            self.data['Time'] = []
            self.data['Pos/[cm]'] = []
            self.data['TOut/[°C]'] = []
            if self.checkSaveT1.isChecked() is True:
                self.data['T1/[°C]'] = []
                self.writeT1.setVisible(True)
            if self.checkSaveT2.isChecked() is True:
                self.data['T2/[°C]'] = []
                self.writeT2.setVisible(True)
            if self.checkSaveT3.isChecked() is True:
                self.data['T3/[°C]'] = []
                self.writeT3.setVisible(True)
            if self.checkSaveT4.isChecked() is True:
                self.data['T4/[°C]'] = []
                self.writeT4.setVisible(True)
            if self.checkSaveP1.isChecked() is True:
                self.data['P1/[Bar]'] = []
                self.writeP1.setVisible(True)
            if self.checkSaveP2.isChecked() is True:
                self.data['P2/[Bar]'] = []
                self.writeP2.setVisible(True)
            for box in self.checkSaveList:
                box.setVisible(False)
            self.stopBtn.setVisible(False)
            self.saveBtn.setText("Stop saving Data")
            self.saveBtn.setStyleSheet("""background-color:red;
                border-radius:10px; font: 12pt "Ubuntu";""")
        else:
            df = pd.DataFrame(data=self.data)
            self.data = {}
            print(df)
            _now = time.time()
            fileName = time.strftime('%Y%m%d%H%M%S', time.localtime(_now))+ '_data.csv'
            path = "/home/pi/Desktop/daten/" + fileName
            f = open(path, 'w')

            f.write(self.kommentar.toPlainText())
            f.write('\n')
            f.close()

            df.to_csv(path, mode='a')
            for i in self.writeList:
                i.setVisible(False)

            for box in self.checkSaveList:
                box.setVisible(True)

            self.saving = False
            self.stopBtn.setVisible(True)
            self.saveBtn.setText("Start saving Data")
            self.saveBtn.setStyleSheet("""background-color:white;
                border-radius:10px; font: 12pt "Ubuntu";""")


    def stopExit(self):
        self.sensors.close()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    try:
        sys.exit(app.exec_())
    except Exception:

        print("Exiting")
