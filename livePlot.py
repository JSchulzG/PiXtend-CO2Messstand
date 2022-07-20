
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
x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    time = data['time']
    t1 = data['T1']
    t2 = data['T2']
    t3 = data['T3']
    t4 = data['T4']
    p1 = data['P1']
    p2 = data['P2']
    pos = data['Pos']
    # print(time)
    plt.cla()

    #axT.plot(time, t1, color='red')
    axT.plot(time, t2, color='red')
    #axT.plot(time, t3, color='green')
    axT.plot(time, t4, color='green')
    axP.plot(time, p1, color='red')
    axT.label_outer()
    axP.label_outer()
    axPos.label_outer()
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()

