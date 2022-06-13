import csv
import glob
import matplotlib.pyplot as plt
import pandas
import sys
import datetime

from pyparsing import empty

#path = '/home/jan/Dokumente/20220612_daten/20220612145925_data.csv'



if __name__ == '__main__':
    path = sys.argv[1]
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
    fig, ax = plt.subplots()
    timeLine = [(datetime.datetime.strptime(time, '%H:%M:%S.%f') - datetime.datetime.strptime(dataFrame['Time'][0], '%H:%M:%S.%f'))/datetime.timedelta(seconds=1) for time in dataFrame['Time'] ]
    for key in dataFrame.keys():
        if key != 'Unnamed: 0' and key != 'Time':
            ax.plot(timeLine, dataFrame[key].values, linewidth=1.5, label=key)
    ax.legend()
    plt.title(title)
    #plt.show()
    pathImg = path.split('.')[0]+'.png'
    plt.savefig(pathImg)
