
import csv
import os
from pathlib import Path
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
"""
TODO
 -refactor
 -layout
"""
plt.style.use('fivethirtyeight')
#fig, (axT, axP, axPos) = plt.subplots(3)
fig = plt.figure()
gs = fig.add_gridspec(3, hspace=0)
axT, axP, axPos = gs.subplots(sharex=True)
fig.suptitle('Live Plot Daten')
start = True
index = count()
fieldnames = ['time', 'T1', 'T2', 'T3', 'T4', 'P1', 'P2', 'Pos']
lengthPlot = 45.0
_plot_ref = {}
time = []
t1 = []
t2 = []
t3 =[]
t4 = []
p1 = []
p2 = []
pos = []

def animate(i):
    if Path('tmp/data.csv').is_file():
        data = pd.read_csv('tmp/data.csv')
        with open('tmp/data2.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        os.remove('tmp/data.csv')
    else:
        data = pd.read_csv('tmp/data2.csv')
        with open('tmp/data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        os.remove('tmp/data2.csv')

    try:
        time.append(data['time'].mean())
    except:
        print('data vault')
        return

    t1.append(round(data['T1'].mean(), 1))
    t2.append(round(data['T2'].mean(), 1))
    t3.append(round(data['T3'].mean(), 1))
    t4.append(round(data['T4'].mean(), 1))
    p1.append(round(data['P1'].mean(), 2))
    p2.append(round(data['P2'].mean(), 2))
    pos.append(round(data['Pos'].mean(), 0))
    #print(time)
    #plt.cla()
    #if start == True:
    #    start_time = time[0]
    #    stat = False
    #    print(start_time)
    #if time[1] > lengthPlot:
    #    axT.set_xlim(time[1]-lengthPlot, time[1])
    #    axP.set_xlim(time[1]-lengthPlot, time[1])
    #    axPos.set_xlim(time[1]-lengthPlot, time[1])
    #axT.plot.clr()
    if len(_plot_ref) == 0:
        _plot_ref['T1'] = axT.plot(time, t1, color='red', marker='.', label='T1')[0]
        _plot_ref['T2'] = axT.plot(time, t2, color='red', marker='.')[0]
        _plot_ref['T3'] = axT.plot(time, t3, color='green', marker='.')[0]
        _plot_ref['T4'] = axT.plot(time, t4, color='green', marker='.')[0]
        _plot_ref['P1'] = axP.plot(time, p1, color='red', marker='.')[0]
        _plot_ref['P2'] = axP.plot(time, p2, color='green', marker='.')[0]
        _plot_ref['Pos'] = axPos.plot(time, pos, color='blue', marker='.')[0]
        axT.set_ylim(10,50)
        axP.set_ylim(30,90)
        axPos.set_ylim(0,20)
    else:
        #axT.autoscale()
        axT.set_xlim(time[0], time[-1])
        #axT.set_ylim()
        axP.set_xlim(time[0], time[-1])
        axPos.set_xlim(time[0], time[-1])
        _plot_ref['T1'].set_data(time, t1)
        _plot_ref['T2'].set_data(time, t2)
        _plot_ref['T3'].set_data(time, t3)
        _plot_ref['T4'].set_data(time, t4)
        _plot_ref['P1'].set_data(time, p1)
        _plot_ref['P2'].set_data(time, p2)
        _plot_ref['Pos'].set_data(time, pos)
    #axT.plot(time, t2, color='red', marker='.')
    #axT.plot(time, t3, color='green', marker='.')
    #axT.plot(time, t4, color='green', marker='.')
    #axP.plot(time, p1, color='red', marker='.')
    #axP.plot(time, p2, color='green', marker='.', linestyle='None')
    #axPos.plot(time, pos, color='blue', marker='.', linestyle='None')
    #axT.label_outer()
    #axP.label_outer()
    #axPos.label_outer()
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=300)

plt.tight_layout()
plt.show()

