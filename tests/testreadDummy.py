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

    def test_read_header(self):
        assert 'T1/[°C]' in self.reader.header()

    def test_get_lenght_of_data(self):
        self.assertEqual(self.reader.getLength(), 98810)

    def test_get_rows(self):
        firstRow = [ 32.9, 29.8, 29.0, 22.2,
                    68.2, 72.0, 42, 2410]
        self.assertListEqual(self.reader.read_Data(), firstRow)
        for i in range(199):
            self.reader.read_Data()
        row200 = [32.1, 27.0, 28.4, 21.6,
                  63.5, 88.7, 42, 2410]
        self.assertListEqual(self.reader.read_Data(), row200)

    def test_has_close(self):
        self.reader.close()

if __name__=='__main__':
    unittest.main()

