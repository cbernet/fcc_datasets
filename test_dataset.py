import unittest
from dataset import Dataset

class TestDataset(unittest.TestCase):

    def test_1(self):
        '''Test dataset creation'''
        dataset = Dataset('papas/ee_to_ZZ_1oct_A_1')
        print dataset

if __name__ == '__main__':
    unittest.main()
