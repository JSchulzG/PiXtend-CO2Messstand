# Co2Messstand
Mit einem PiXtendV2L werden 4 Temperaturen, 2 Drücke und eine Position ausgelesen.
Die Temperaturen werden mit PT100 und Messverstärkern aufgenommen. Die Drücke mit zwei PN3571.
Die Position wird mit einem TFMini-S Lidar und einer USB-TTL Schnittstelle bestimmt.
Die graphische Oberfläche wurde mit PyQt5 geschrieben und mit dem Python-Modul pixtendv2l werden die Daten vom PiXtend geholt.
Der Messintervall beträgt 50ms.

![coMessstand](https://user-images.githubusercontent.com/76759916/173206324-08c9684a-6e17-4d6a-8969-e8e1965ae27e.png)




# Co2MessstandPlot
In dieser Version werden die Daten geplottet. Da der Plot aber bis zu 500ms braucht, werden die Daten während der Datenaufzeichnung nicht geplottet.

![coMessstandPlot_2](https://user-images.githubusercontent.com/76759916/173206293-6ed0a210-844c-42b4-b547-dc1d914e2fc8.png)
