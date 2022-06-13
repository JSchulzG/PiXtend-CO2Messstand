import csv
import glob
import matplotlib.pyplot as plt
import pandas
import sys
import datetime

from pyparsing import empty


def plot(path, show=False, save=True):
    print(path)
    file = open(path)
    startData = 0
    title = ''
    while True:
        line = file.readline()
        if 'Time,Pos/[cm]' in line:
            break
        if line != '\n':
            title += line
            startData += 1
    print(title)
    dataFrame = pandas.read_csv(path, header=startData)
    fig, (axT, axP, axS) = plt.subplots(3, sharex=True, gridspec_kw={'hspace': 0})
    timeLine = [(datetime.datetime.strptime(time, '%H:%M:%S.%f') - datetime.datetime.strptime(dataFrame['Time'][0], '%H:%M:%S.%f'))/datetime.timedelta(seconds=1) for time in dataFrame['Time'] ]
    for key in dataFrame.keys():
        if key != 'Unnamed: 0' and key != 'Time':
            if '°C' in key:
                axT.plot(timeLine, dataFrame[key].values, linewidth=1.5, label=key)
                axT.set(ylabel='°C')
            if 'Bar' in key:
                axP.plot(timeLine, dataFrame[key].values, linewidth=1.5, label=key)
                axP.set(ylabel='Bar')
            if 'cm' in key:
                axS.plot(timeLine, dataFrame[key].values, linewidth=1.5, label=key)
                axS.set(ylabel='cm')
    
    axT.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    axP.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    axS.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Zeit in Sekunden')
    
    fig.suptitle(title)
    plt.tight_layout()
    if show == True:
        plt.show()
    if save == True:
        pathImg = path.split('.')[0]+'_new.png'
        plt.savefig(pathImg)

if __name__ == '__main__':
    path = sys.argv[1]
    plot(path, show=True, save=False)
