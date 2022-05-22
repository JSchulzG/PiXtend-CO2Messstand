# This Python file uses the following encoding: utf-8
import time
import os
from pathlib import Path
import pandas as pd
import sys


import readTempData
import dummi_readSensorData as rSD

#import matplotlib
#matplotlib.use('Qt5Agg')
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.ticker as ticker
import numpy as np


from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer


"""
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.fig.tight_layout()
        self.axes.set_ylabel('T / [°C]')
"""
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = self.load_ui()
        self.writeList = [self.writeT1, self.writeT2, self.writeT3, self.writeT4, self.writeP1, self.writeP1, self.writeP2]
        for i in self.writeList:
            i.setVisible(False)
        self.checkSaveList = [self.checkSaveT1, self.checkSaveT2, self.checkSaveT3, self.checkSaveT4, self.checkSaveP1, self.checkSaveP2]

        self.valueT1.setText('%.1f °C' % 0)
        self.valueT2.setText('%.1f °C' % 0)
        self.valueT3.setText('%.1f °C' % 0)
        self.valueT4.setText('%.1f °C' % 0)
        self.sensorList = [self.valueT1, self.valueT2, self.valueT3, self.valueT4, self.valueP1, self.valueP2]
        #self.step = 0
        #self.step_plot = 0
        self.value = 0.0
        self.saving = None
        self.d = {}
        self.qTimer = QTimer()
        self.qTimer.setInterval(50)  # 50ms max PiXtend is not as fast :(
        self.qTimer.timeout.connect(self.getSensorData)
        self.qTimer.start()
        self.saveBtn.clicked.connect(self.writeData)
        self.stopBtn.clicked.connect(self.stopExit)
        #self.canvas = MplCanvas(self)
        #l = QVBoxLayout(self.plot2Widget)
        #l.addWidget(self.canvas)
        self.temp1 = readTempData.ReadTempData()
        #self.dummiSensor = rSD.ReadTemperature()
    """
    def plotUpdate(self):
        try:
            #self.plotdataT1 = np.vstack((self.plotdataT1, float(self.valueT1.text().split(' ')[0])))[-5:]
            #self.plotdataT2 = np.vstack((self.plotdataT2, float(self.valueT2.text().split(' ')[0])))[-5:]
            self.plotdataT3 = np.vstack((self.plotdataT3, float(self.valueT3.text().split(' ')[0])))[-5:]
            self.plotdataT4 = np.vstack((self.plotdataT4, float(self.valueT4.text().split(' ')[0])))[-5:]
            self.plotdataP1 = np.vstack((self.plotdataP1, float(self.valueP1.text().split(' ')[0])))[-5:]
            self.plotdataP2 = np.vstack((self.plotdataP2, float(self.valueP2.text().split(' ')[0])))[-5:]

        except:
            # first data point
            print('except')
            #self.plotdataT1 = np.array([[(float(self.valueT1.text().split(' ')[0]))]])
            #self.plotdataT2 = np.array([[(float(self.valueT2.text().split(' ')[0]))]])
            self.plotdataT3 = np.array([[(float(self.valueT3.text().split(' ')[0]))]])
            self.plotdataT4 = np.array([[(float(self.valueT4.text().split(' ')[0]))]])
            self.plotdataP1 = np.array([[(float(self.valueP1.text().split(' ')[0]))]])
            self.plotdataP2 = np.array([[(float(self.valueP2.text().split(' ')[0]))]])
        #self.ydata = self.plotdata

        self.canvas.axes.clear()
        self.canvas.axes.set_facecolor((0, 0, 0))
        self.canvas.axes.yaxis.grid(True, linestyle='--')
        start, end = self.canvas.axes.get_ylim()
        self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        self.canvas.axes.set_autoscale_on(True)  #set_ylim( ymin=0, ymax=100)
        #self.canvas.axes.plot(self.plotdataT1, color=(0,1,0.29))
        #self.canvas.axes.plot(self.plotdataT2, color=(0,1,0))
        self.canvas.axes.plot(self.plotdataT3, color=(1,0,0.29))
        self.canvas.axes.plot(self.plotdataT4, color=(1,0,0))
        self.canvas.axes.plot(self.plotdataP1, color=(0,1,1))
        self.canvas.axes.plot(self.plotdataP2, color=(0,1,1))
        self.canvas.draw()
        self.canvas.flush_events()
        """

    def load_ui(self):
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        loadUi(path, self)

    def getSensorData(self):
        """
        Das macht so keinen Sinn mit der Schleife, da jedesmal alle Daten geholt werden.
        Sehr viel Zeitverschwendung!!!
        ToDo: die Werte jede Runde an sensorList uebergeben und ggf. speichern.
        """
        #self.value = self.dummiSensor.getData()
        self.value = self.temp1.read_Data()
        for i in range(6):
            if i < 4:
                self.sensorList[i].setText('%.1f °C' % self.value[i])
            else:
                self.sensorList[i].setText('%.1f Bar' % self.value[i])
        # self.sensorList[self.step].setText('%.1f °C' % self.value[self.step])
        if self.saving is True:
            _now = time.time()
            t = time.strftime('%Y%m%d %X', time.localtime(_now)) + ':' + str('%.3f' % _now).split('.')[1]
            self.d['Time'].append(t)
            if self.checkSaveT1.isChecked() is True:
                self.d['T1 / [°C]'].append(self.valueT1.text().split(' ')[0])
            if self.checkSaveT2.isChecked() is True:
                self.d['T2 / [°C]'].append(self.valueT2.text().split(' ')[0])
            if self.checkSaveT3.isChecked() is True:
                self.d['T3 / [°C]'].append(self.valueT3.text().split(' ')[0])
            if self.checkSaveT4.isChecked() is True:
                self.d['T4 / [°C]'].append(self.valueT4.text().split(' ')[0])
            if self.checkSaveP1.isChecked() is True:
                self.d['P1 / [Bar]'].append(self.valueP1.text().split(' ')[0])
            if self.checkSaveP2.isChecked() is True:
                self.d['P2 / [Bar]'].append(self.valueP2.text().split(' ')[0])


        #self.step += 1
        #self.step_plot += 1
        """            if self.checkSaveP1.isChecked() is True:
            self.d['P1 / [Bar]'] = []
            self.writeP1.setVisible(True)

        if self.step_plot >10:
            self.plotUpdate()
            self.step_plot = 0

        """


    def writeData(self):
        if self.saving is False or self.saving is None:
            self.saving = True
            self.d['Time'] = []
            if self.checkSaveT1.isChecked() is True:
                self.d['T1 / [°C]'] = []
                self.writeT1.setVisible(True)
            if self.checkSaveT2.isChecked() is True:
                self.d['T2 / [°C]'] = []
                self.writeT2.setVisible(True)
            if self.checkSaveT3.isChecked() is True:
                self.d['T3 / [°C]'] = []
                self.writeT3.setVisible(True)
            if self.checkSaveT4.isChecked() is True:
                self.d['T4 / [°C]'] = []
                self.writeT4.setVisible(True)
            if self.checkSaveP1.isChecked() is True:
                self.d['P1 / [Bar]'] = []
                self.writeP1.setVisible(True)
            if self.checkSaveP2.isChecked() is True:
                self.d['P2 / [Bar]'] = []
                self.writeP2.setVisible(True)
            for box in self.checkSaveList:
                box.setVisible(False)

            self.saveBtn.setText("Stop saving Data")
            self.saveBtn.setStyleSheet("""background-color:red;
                border-radius:10px; font: 12pt "Ubuntu";""")
        else:
            df = pd.DataFrame(data=self.d)
            self.d = {}
            print(df)
            _now = time.time()
            fileName = time.strftime('%Y%m%d%H%M%S', time.localtime(_now))+ '_data.csv'

            #path = os.fspath(Path(__file__).resolve().parent / "data" / fileName)
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
            self.saveBtn.setText("Start saving Data")
            self.saveBtn.setStyleSheet("""background-color:white;
                border-radius:10px; font: 12pt "Ubuntu";""")


    def stopExit(self):
        self.temp1.close()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    try:
        sys.exit(app.exec_())
    except Exception:

        print("Exiting")
