import pandas
from pathlib import Path

class ReadFile:
    def __init__(self, path):
        self._path = Path(path)
        if path[-4:] != '.csv':
            raise Exception('Data has to be *.csv file')
        elif self._path.is_file() == False:
            raise Exception('file doesn\'t exists')



