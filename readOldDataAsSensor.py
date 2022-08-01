import pandas
from pathlib import Path

class ReadFile:
    def __init__(self, path):
        self._path = Path(path)
        if path[-4:] != '.csv':
            raise Exception('Data has to be *.csv file')
        elif self._path.is_file() == False:
            raise Exception('file doesn\'t exists')
        self.dataFrame = pandas.read_csv(self._path)
        self.rowCount = 0

    def header(self):
        return list(self.dataFrame.columns)

    def getLength(self):
        return self.dataFrame.size

    def read_Data(self):
        row = []
        keys = ['T1/[°C]', 'T2/[°C]', 'T3/[°C]', 'T4/[°C]',
                'P1/[Bar]', 'P2/[Bar]', 'Pos/[cm]', 'TOut/[°C]']
        for key in keys:
            if key == 'Pos/[cm]':
                row.append(self.dataFrame.iloc[self.rowCount][key]+25)
            elif key == 'TOut/[°C]':
                row.append(self.dataFrame.iloc[self.rowCount][key]*100)
            else:
                row.append(self.dataFrame.iloc[self.rowCount][key])
        if self.rowCount < self.getLength():
            self.rowCount += 1
        else:
            self.rowCount = 0
        return row

    def close(self):
        del self.dataFrame
        del self._path
        del self.rowCount

