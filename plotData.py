
import matplotlib.pyplot as plt
import pandas

path = '/home/jan/Dokumente/20220612_daten/20220612145925_data.csv'

dataFrame = pandas.read_csv(path, header=1)
fig, ax = plt.subplots()
for key in dataFrame.keys():
    if key != 'Unnamed: 0' and key != 'Time':
        ax.plot(dataFrame[key], linewidth=1.5, label=key)

ax.legend()
#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
 #      ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()