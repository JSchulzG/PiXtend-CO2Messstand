import csv
import os
from pathlib import Path
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
#fig, (axT, axP, axPos) = plt.subplots(3)
fig = plt.figure()
gs = fig.add_gridspec(3, hspace=0)
axT, axP, axPos = gs.subplots(sharex=True)
fig.suptitle('Live Plot Daten')
start = True
index = count()
fieldnames = ['time', 'T1', 'T2', 'T3', 'T4', 'P1', 'P2', 'Pos']
lengthPlot = 20.0

def animate(i):
    if Path('data.csv').is_file():
        data = pd.read_csv('data.csv')
        with open('data2.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        os.remove('data.csv')
    else:
        data = pd.read_csv('data2.csv')
        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        os.remove('data2.csv')

    try:
        time = data['time']
    except:
        print('data vault')
        return
    t1 = data['T1']
    t2 = data['T2']
    t3 = data['T3']
    t4 = data['T4']
    p1 = data['P1']
    p2 = data['P2']
    pos = data['Pos']
    #print(time)
    #plt.cla()
    #if start == True:
    #    start_time = time[0]
    #    stat = False
    #    print(start_time)
    if time[1] > lengthPlot:
        axT.set_xlim(time[1]-lengthPlot, time[1])
        axP.set_xlim(time[1]-lengthPlot, time[1])
        axPos.set_xlim(time[1]-lengthPlot, time[1])

    axT.plot(time, t1, color='red', marker='.', label='T1')
    axT.plot(time, t2, color='red', marker='.')
    axT.plot(time, t3, color='green', marker='.')
    axT.plot(time, t4, color='green', marker='.')
    axP.plot(time, p1, color='red', marker='.')
    axP.plot(time, p2, color='green', marker='.')
    axPos.plot(time, pos, color='blue', marker='.', linestyle='None')
    axT.label_outer()
    axP.label_outer()
    axPos.label_outer()
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=300)

plt.tight_layout()
plt.show()

