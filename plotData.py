import matplotlib.pyplot as plt
import pandas
import sys
import datetime

path = '/home/jan/Dokumente/20220612_daten/20220612145925_data.csv'
#path = sys.argv[1]
print(path)
dataFrame = pandas.read_csv(path, header=1)
fig, ax = plt.subplots()
timeLine = [(datetime.datetime.strptime(time, '%H:%M:%S.%f') - datetime.datetime.strptime(dataFrame['Time'][0], '%H:%M:%S.%f'))/datetime.timedelta(seconds=1) for time in dataFrame['Time'] ]
for key in dataFrame.keys():
    if key != 'Unnamed: 0' and key != 'Time':
        ax.plot(timeLine, dataFrame[key].values, linewidth=1.5, label=key)
print(datetime.datetime.strptime(dataFrame['Time'][2], '%H:%M:%S.%f')- datetime.datetime.strptime(dataFrame['Time'][1], '%H:%M:%S.%f'))
ax.legend()
#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
 #      ylim=(0, 8), yticks=np.arange(1, 8))
print(dataFrame['T1/[°C]'].values)
plt.show()