import plotData
import glob

listFiles = glob.glob("/home/jan/Nextcloud/CO2-Motor/Technik-AG/4 - Messungen/20220612 (Jungfernlauf)/*.csv")

for file in listFiles:
    plotData.plot(file, save=True, show=False)
