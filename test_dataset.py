import unittest
from dataset import Dataset

class TestDataset(unittest.TestCase):

    def test_1_create(self):
        '''Test dataset creation'''
        dataset = Dataset('papas/ee_to_ZZ_1oct_A_1','*0_1*.root', cache=False)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset('papas/ee_to_ZZ_1oct_A_1','*0_1*.root', cache=True)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)



if __name__ == '__main__':
    unittest.main()
