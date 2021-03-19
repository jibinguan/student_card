import unittest
import main

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass\n\n')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_pandas(self):
        filename = 'courses.csv'
        data = main.pd.read_csv(filename, index_col=0)
        print("test pandas is OK")

    def test_json(self):
        with open('output.json', 'r') as f:
            load_dict = main.json.load(f)
            print(load_dict)
        print("test json is OK")

    def test_load_from_cvs(self):
        filename = 'courses.csv students.csv tests.csv marks.csv'
        main.load_from_cvs(filename)
        print("test load_from_cvs() arguments")



if __name__ == '__main__':
    unittest.main()
