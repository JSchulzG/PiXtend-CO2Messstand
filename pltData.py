import time
import os
from pathlib import Path
import sys



import matplotlib.pyplot as plt

"""
class PlotWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = self.load_ui()
        #plt.ion()
        self.timeSeries = []
        self.t1Series = []
        self.canvas = MplCanvas(self)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(self.canvas)
        self._plot_ref = {}
        app = QApplication(sys.argv)
        #widget = MainWindow()
        #self.show()

    def load_ui(self):
        path = os.fspath(Path(__file__).resolve().parent / "formPlot.ui")
        loadUi(path, self)
    """

class GetData:
    #def __init__(self):
        #plt.ion()
        #self.fig = plt.figure()
        #self.axes = self.fig.add_subplot(111)
        #self.i = 0
    def getData(self, queueData):
        i = 0
        while True:
            data = queueData.get()
            print(i)
            #self.axes.plot(self.i, 10)
            #self.fig.draw()
            plt.scatter(i, i, marker='*')
            plt.show()
            #plt.pause(0.01)
            i += 1
            #self.timeSeries.append(data[0])
            #self.t1Series.append(data[1])
            #self.t1Series = self.timeSeries[-500:]
            #self.t1Series = self.t1Series[-500:]
            #print(len(self.t1Series))
            #print(len(self.timeSeries))
            """
            if len(self._plot_ref) == 0:
                self.canvas.axes.set_facecolor((0, 0, 0))
                self.canvas.axes.yaxis.grid(True, linestyle='--')
                self.canvas.axes.set_xlim(0, 10)
                self.canvas.axes.set_ylim(0, 100)
                plotT1_refs = self.canvas.axes.plot(self.timeSeries ,self.t1Series, color=(0,1,0.29))
                print(plotT1_refs[0])
                self._plot_ref['T1'] = plotT1_refs[0]
            else:
                self._plot_ref['T1'].set_data(self.timeSeries, self.t1Series)

            self.canvas.draw()
            #self.line1.set_ydata(self.t1Series)
            #self.line1.set_xdata(self.timeSeries)
            #self.fig.canvas.draw()
            #self.fig.canvas.flush_events()
            #plt.scatter(data[0], data[1])
            """
            if data == 'done and exit':
                break
