import unittest
from dataset import Dataset

dataset_name = 'papas/ee_to_ZZ_1oct_A_1'
dataset_pattern = '*.0_1*.root'

class TestDataset(unittest.TestCase):

    def test_1_create(self):
        '''Test dataset creation'''
        dataset = Dataset(dataset_name, dataset_pattern, cache=False)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)

    def test_3_print(self):
        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
        printout = '''papas/ee_to_ZZ_1oct_A_1
/eos/experiment/fcc/ee/datasets/papas/ee_to_ZZ_1oct_A_1
papasout_2.0_15.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_12.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_18.root           : {'good': False, 'n_events': None, 'zero_size': True}
papasout_2.0_17.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_1.root            : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_11.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_14.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_13.root           : {'good': False, 'n_events': None, 'zero_size': True}
papasout_2.0_19.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_16.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
papasout_2.0_10.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}'''
        self.assertMultiLineEqual(str(dataset),printout)



if __name__ == '__main__':
    unittest.main()
