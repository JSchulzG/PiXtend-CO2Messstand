
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import pandas
import sys
import datetime
import numpy as np
from pyparsing import empty


def plot(path, show=False, save=True):
    print(path)
    if '.csv' != path[-4:]:
        print('bitte eine csv Datei übergeben!')
        return

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
    timeLine = [(datetime.datetime.strptime(time, '%H:%M:%S.%f') - 
                 datetime.datetime.strptime(dataFrame['Time'][0], 
                 '%H:%M:%S.%f'))/datetime.timedelta(seconds=1) for time in dataFrame['Time'] ]
    dataFrame['Time'] = timeLine
    dataFrame.set_index('Time', inplace=True)
    for key in dataFrame.keys():
        if key != 'Unnamed: 0' and key != 'Time':
            if '°C' in key:
                axT.plot(dataFrame[key], linewidth=1.5, label=key)
                axT.set(ylabel='°C')
            if 'Bar' in key:
                axP.plot(dataFrame[key], linewidth=1.5, label=key)
                axP.set(ylabel='Bar')
            if 'cm' in key:
                axS.plot(dataFrame[key], linewidth=1.5, label=key)
                axS.set(ylabel='cm')

    # Bestimmung der lokalen Minima 
    dataFrame['min'] = dataFrame.iloc[argrelextrema(dataFrame['Pos/[cm]'].values, np.less_equal,
                    order=2000)[0]]['Pos/[cm]']
    #axS.scatter(dataFrame.index, dataFrame['min'], c='r')
    dataFrame['max'] = dataFrame.iloc[argrelextrema(dataFrame['Pos/[cm]'].values, np.greater_equal,
                    order=2000)[0]]['Pos/[cm]']
    #axS.scatter(dataFrame.index, dataFrame['max'], c='g')
    # Bestimmung der Zykluszeit von erstem lokalen Min zu dem nächsten.
    # D.h. Zeit die der Kolben braucht um von links nach rechts und zurück zu fahren.
    # Daraus liesse sich die Leistung berechnen.
    deltaTime = 0.0
    startTime = 0.0
    dataFrame['startZyklus'] = np.nan
    for time in dataFrame.index:
        if dataFrame['min'][time] >= 0 and startTime == 0.0:
            #print(time)
            startTime = time
            dataFrame.at[time, 'startZyklus'] = dataFrame['min'][time]
        elif dataFrame['min'][time] >= 0 and deltaTime < 40.0:
            deltaTime = time - startTime
        elif dataFrame['min'][time] >= 0 and deltaTime >40.0:
            deltaTime = time - startTime
            print('Zyklus Zeit: %.3f' %deltaTime)
            dataFrame.at[time, 'startZyklus'] = dataFrame['min'][time]
            startTime = time
            deltaTime = 0.0
    axS.scatter(dataFrame.index, dataFrame['startZyklus'], c='r')
    for time in dataFrame.index:
        if dataFrame['startZyklus'][time] != np.nan:
            axS.annotate('%.1f'%time, (time-40, dataFrame['startZyklus'][time]))
        
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
