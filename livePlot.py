
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
fig = plt.figure(tight_layout=False)
gs = fig.add_gridspec(3, hspace=0.1)
axT, axP, axPos = gs.subplots(sharex=True)
axT.set(ylabel='°C')
axP.set(ylabel='Bar')
axPos.set(ylabel='cm')
fig.suptitle('Live Plot Daten')
fieldnames = ['time', 'T1', 'T2', 'T3', 'T4', 'P1', 'P2', 'Pos']
_plot_ref = {}
time = []
t1 = []
t2 = []
t3 =[]
t4 = []
p1 = []
p2 = []
pos = []

tMin = 50
tMax = 10
pMin = 60
pMax = 10
dataDict = {'time': time,'T1': t1, 'T2': t2, 'T3': t3,
            'T4': t4, 'P1': p1, 'P2': p2, 'Pos': pos}

def animate(i): #, tMin, tMax, pMin, pMax):
    tMin, tMax = axT.get_ylim()
    pMin, pMax = axP.get_ylim()
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
    for row in fieldnames:
        x = round(data[row].mean(),1)
        if 'T' in row and (x<tMin):
            tMin = x-2
        if 'T' in row and tMax < x: tMax = x+2
        if 'Pos' not in row:
            if 'P' in row and pMin > x: pMin = x-2
            if 'P' in row and pMax < x: pMax = x+2
        if 'time' not in row:
            dataDict[row].append(x)

    if len(_plot_ref) == 0:
        _plot_ref['T1'] = axT.plot(time, t1, color='#ff5000', marker='.', label='T1')[0]
        _plot_ref['T2'] = axT.plot(time, t2, color='#ff0000', marker='.', label='T2')[0]
        _plot_ref['T3'] = axT.plot(time, t3, color='#30f', marker='.', label='T3')[0]
        _plot_ref['T4'] = axT.plot(time, t4, color='#328', marker='.', label='T4')[0]
        _plot_ref['P1'] = axP.plot(time, p1, color='red', marker='.', label='P1')[0]
        _plot_ref['P2'] = axP.plot(time, p2, color='#60f', marker='.', label='P2')[0]
        _plot_ref['Pos'] = axPos.plot(time, pos, color='blue', marker='.', label='Position')[0]
        #axT.set_ylim(20,45)
        axP.set_ylim(60,62)
        axPos.set_ylim(0,20)
    else:
        axT.set_xlim(time[0], time[-1])
        axT.set_ylim(tMin, tMax)
        axP.set_xlim(time[0], time[-1])
        axP.set_ylim(pMin, pMax)
        axPos.set_xlim(time[0], time[-1])
        _plot_ref['T1'].set_data(time, t1)
        _plot_ref['T2'].set_data(time, t2)
        _plot_ref['T3'].set_data(time, t3)
        _plot_ref['T4'].set_data(time, t4)
        _plot_ref['P1'].set_data(time, p1)
        _plot_ref['P2'].set_data(time, p2)
        _plot_ref['Pos'].set_data(time, pos)
    axT.legend(loc='center left', bbox_to_anchor=(0, 0.5))
    axP.legend(loc='center left', bbox_to_anchor=(0, 0.5))
    axPos.legend(loc='center left', bbox_to_anchor=(0, 0.5))

ani = FuncAnimation(plt.gcf(), animate, interval=300)# fargs=(tMin, tMax, pMin, pMax), interval=300)

plt.show()

