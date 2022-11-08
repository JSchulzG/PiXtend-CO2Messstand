# This Python file uses the following encoding: utf-8
import time
import os
from pathlib import Path
import sys
from os.path import exists
import pandas as pd

import csv
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QProcess
import matplotlib
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import readSensorData
#import readDummySensors as rSD
#import readOldDataAsSensor as rOD

"""
GUI for Messurement with PiXtendV2L
"""


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = self.load_ui()
        self.writeList = [self.writeT1, self.writeT2,
                          self.writeT3, self.writeT4,
                          self.writeP1, self.writeP1,
                          self.writeP2]
        for i in self.writeList:
            i.setVisible(False)
        self.checkSaveList = [self.checkSaveT1, self.checkSaveT2,
                              self.checkSaveT3, self.checkSaveT4,
                              self.checkSaveP1, self.checkSaveP2]

        self.sliderPosition.setMinimum(1)
        self.sliderPosition.setMaximum(17)

        self.valueT1.setText('%.1f °C' % 0)
        self.valueT2.setText('%.1f °C' % 0)
        self.valueT3.setText('%.1f °C' % 0)
        self.valueT4.setText('%.1f °C' % 0)
        self.sensorList = [self.valueT1, self.valueT2, self.valueT3,
                           self.valueT4, self.valueP1, self.valueP2]
        self.sensorDict = {'T1': self.valueT1, 'T2': self.valueT2, 'T3': self.valueT3,
                           'T4': self.valueT4, 'P1': self.valueP1, 'P2': self.valueP2,
                           'Pos': self.valuePosition}
        self.value = 0.0
        self.saving = None
        self.startPlotTime = time.time()
        self.data = {}
        self.qTimer = QTimer()
        self.qTimer.setInterval(50)  # 50ms max PiXtend is not as fast :(
        self.qTimer.timeout.connect(self.getSensorData)
        self.qTimer.start()
        self.saveBtn.clicked.connect(self.writeData)
        self.stopBtn.clicked.connect(self.stopExit)
        self.sensors = readSensorData.ReadSensorData()
        #self.sensors = rSD.ReadSensorData()
        #self.sensors = rOD.ReadFile(
        #    '/home/user/Documents/MessDaten/20220612/20220612162738_data.csv')
        self.fieldnames = ['time'] + list(self.sensorDict.keys())
        with open('tmp/data.csv','w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
        self.process = None
        self.plotData.pressed.connect(self.startPlot)
        self.leftWarm.pressed.connect(self.sensors.heatLeftSide)
        self.leftCold.pressed.connect(self.sensors.coldLeftSide)
        self.rightWarm.pressed.connect(self.sensors.heatRightSide)
        self.rightCold.pressed.connect(self.sensors.coldRightSide)

    def startPlot(self):
        if self.process is None:
            self.process = QProcess()
            self.process.finished.connect(self.process_finished)
            self.process.start("python3", ['livePlot.py'])

    def process_finished(self):
        self.process = None

    def writeTempFile(self):
        if Path('tmp/data.csv').is_file():
            path = 'tmp/data.csv'
        else:
            path = 'tmp/data2.csv'
        with open(path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            _time = time.time() - self.startPlotTime
            data = {}
            for key in self.fieldnames:
                if key == 'time':
                    data[key] = _time
                else:
                    data[key] = self.sensorDict[key].text().split(' ')[0]
            csv_writer.writerow(data)

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
        self.writeTempFile()

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

            self.saveBtn.setText("Stop saving Data")
            self.saveBtn.setStyleSheet("""background-color:red;
                border-radius:10px; font: 12pt "Ubuntu";""")
        else:
            df = pd.DataFrame(data=self.data)
            self.data = {}
            print(df)
            _now = time.time()
            fileName = time.strftime('%Y%m%d%H%M%S', time.localtime(_now))+ '_data.csv'
            path = "/home/pi/Dokumente/daten/" + fileName
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
            self.saveBtn.setText("Start saving Data")
            self.saveBtn.setStyleSheet("""background-color:white;
                border-radius:10px; font: 12pt "Ubuntu";""")

    def stopExit(self):
        #self.queueData.put('done and exit')
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
