import unittest
import readOldDataAsSensor as readData


class TestDummyData(unittest.TestCase):
    def setUp(self):
        self.reader = readData.ReadFile('/home/user/Documents/MessDaten/20220612/20220612162738_data.csv')

    def test_file_exists_and_is_csv(self):
        with self.assertRaises(Exception) as context:
            readData.ReadFile('medaten.csv')
        self.assertTrue('file doesn\'t exists' in str(context.exception))
        with self.assertRaises(Exception) as context:
            readData.ReadFile('messdaten')
        self.assertTrue('Data has to be *.csv file' in str(context.exception))

if __name__=='__main__':
    unittest.main()

