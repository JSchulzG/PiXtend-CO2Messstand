# This Python file uses the following encoding: utf-8
import time
import os
from pathlib import Path
import pandas as pd
import sys

#import readSensorData
import readDummySensors as rSD
import csv

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

from multiprocessing import Process, Queue
from pltData import GetData

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.fig.tight_layout()
        self.axes.set_ylabel('T / [°C]')

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
        self.step = 0
        self.step_plot = 0
        self.value = 0.0
        self.saving = None
        self._plot_ref = {}
        self.plotDataTime = []
        self.plotDataT1 = []
        self.plotDataT2 = []
        self.plotDataT3 = []
        self.plotDataT4 = []
        self.plotDataP1 = []
        self.plotDataP2 = []
        self.plotDataPos = []
        # self.plotLength = 500

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
        #self.queueData = Queue()
        """
        start with multiprocessing see:
        https://stackoverflow.com/questions/43861164/passing-data-between-separately-running-python-scripts

        """
        self.fieldnames = ['time', 'T1', 'T2']
        with open('data.csv','w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()
        #ploter = GetData()
        #pltData = Process(target=ploter.getData, args=[self.queueData])
        #pltData.deamon = True
        #pltData.start()
        self.startPlotTime = time.time()

    def writeTempFile(self):
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            _time = time.time() - self.startPlotTime
            data = {
                "time": _time,
                "T1": self.sensorList[0].text().split(' ')[0],
                "T2": self.sensorList[1].text().split(' ')[0]
            }
            csv_writer.writerow(data)
        #dataLine = [float(_time)]
        #for sensor in self.sensorList:
         #   dataLine.append(float(sensor.text().split(' ')[0]))
        #print(dataLine)
        #self.queueData.put(dataLine)

    """
    def plotUpdate(self):
        _time = time.time()-self.startPlotTime
        self.plotDataTime.append(_time)
        self.plotDataT1.append(float(self.valueT1.text().split(' ')[0]))
        self.plotDataT2.append(float(self.valueT2.text().split(' ')[0]))
        self.plotDataT3.append(float(self.valueT3.text().split(' ')[0]))
        self.plotDataT4.append(float(self.valueT4.text().split(' ')[0]))
        self.plotDataP1.append(float(self.valueP1.text().split(' ')[0]))
        self.plotDataP2.append(float(self.valueP2.text().split(' ')[0]))
        self.plotDataPos.append(float(self.valuePosition.text().split(' ')[0]))

        if len(self._plot_ref) == 0:
            self.canvas.axes.set_facecolor((0, 0, 0))
            self.canvas.axes.yaxis.grid(True, linestyle='--')
            self.canvas.axes.set_xlim(0, 10)
            self.canvas.axes.set_ylim(0, 100)
            plotT1_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataT1, color=(0,1,0.29))
            print(plotT1_refs[0])
            self._plot_ref['T1'] = plotT1_refs[0]
            plotT2_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataT2, color=(0,1,0))
            self._plot_ref['T2'] = plotT2_refs[0]
            plotT3_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataT3, color=(1,0,0.29))
            self._plot_ref['T3'] = plotT3_refs[0]
            plotT4_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataT4, color=(1,0,0))
            self._plot_ref['T4'] = plotT4_refs[0]
            plotP1_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataP1, color=(0,1,1))
            self._plot_ref['P1'] = plotP1_refs[0]
            plotP2_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataP2, color=(0,1,1))
            self._plot_ref['P2'] = plotP2_refs[0]
            plotPos_refs = self.canvas.axes.plot(self.plotDataTime, self.plotDataPos, color=(1,1,1))
            self._plot_ref['Pos'] = plotPos_refs[0]
        else:
            if len(self.plotDataTime) < self.plotLength.value():
                self.canvas.axes.set_xlim(0, self.plotDataTime[-1])
            else:
                self.canvas.axes.set_xlim(self.plotDataTime[-self.plotLength.value()], self.plotDataTime[-1])
            if self.checkSaveT1.isChecked() is True:
            #if self.step_plot == 0 and self.checkSaveT1.isChecked() is True:
                self._plot_ref['T1'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataT1[-self.plotLength.value():])
            if self.checkSaveT2.isChecked() is True:
            #if self.step_plot == 1 and self.checkSaveT2.isChecked() is True:
                self._plot_ref['T2'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataT2[-self.plotLength.value():])
            if self.checkSaveT3.isChecked() is True:
            #if self.step_plot == 2 and self.checkSaveT3.isChecked() is True:
                self._plot_ref['T3'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataT3[-self.plotLength.value():])
            if self.checkSaveT4.isChecked() is True:
            #if self.step_plot == 3 and self.checkSaveT4.isChecked() is True:
                self._plot_ref['T4'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataT4[-self.plotLength.value():])
            if self.checkSaveP1.isChecked() is True:
            #if self.step_plot == 4 and self.checkSaveP1.isChecked() is True:
                self._plot_ref['P1'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataP1[-self.plotLength.value():])
            if self.checkSaveP2.isChecked() is True:
            #if self.step_plot == 5 and self.checkSaveP2.isChecked() is True:
                self._plot_ref['P2'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataP2[-self.plotLength.value():])
            #if self.step_plot == 6:
            self._plot_ref['Pos'].set_data(self.plotDataTime[-self.plotLength.value():], self.plotDataPos[-self.plotLength.value():])
            self.step_plot = 0
            #else:
            #   self.step_plot += 1
        self.step = 0
        self.canvas.draw()
        #self.canvas.flush_events()
    """

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
        #if self.step > :
        #self.plotUpdate()
        #self.step += 1
        #self.step_plot += 1
        """            if self.checkSaveP1.isChecked() is True:
            self.data['P1 / [Bar]'] = []
            self.writeP1.setVisible(True)

        if self.step_plot >10:
            self.plotUpdate()
            self.step_plot = 0

        """


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
            path = "/home/user/Documents/daten/" + fileName
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
