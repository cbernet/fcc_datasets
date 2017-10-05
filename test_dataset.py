import unittest
import os
import basedir
from dataset import Dataset

if not os.path.isdir(basedir.basename):
    basedir.basename = os.path.abspath('test')
dataset_name = 'papas/ee_to_ZZ_1oct_A_1'
cfg_name = 'test/analysis_test_cfg.py'
dataset_pattern = '*.0_1*.root'

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset(dataset_name, dataset_pattern, cache=False,
                               cfg=cfg_name, xsection=1.8e-9)        

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files),11)
        self.assertEqual(len(self.dataset.list_of_good_files()),9)
        self.assertEqual(self.dataset.nfiles(), 11)
        self.assertEqual(self.dataset.ngoodfiles(), 9)
        self.dataset.write_yaml()

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
        self.assertEqual(dataset.nevents(), 900000)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
        data_written = dataset.write_yaml()
        data_read = dataset.read_yaml()
        self.assertDictEqual(data_written, data_read)
        
        
        
        
##    def test_3_print(self):
##        dataset = Dataset(dataset_name, dataset_pattern, cache=True)
##        printout = '''papas/ee_to_ZZ_1oct_A_1
##/eos/experiment/fcc/ee/datasets/papas/ee_to_ZZ_1oct_A_1
##papasout_2.0_15.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_12.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_18.root           : {'good': False, 'n_events': None, 'zero_size': True}
##papasout_2.0_17.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_1.root            : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_11.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_14.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_13.root           : {'good': False, 'n_events': None, 'zero_size': True}
##papasout_2.0_19.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_16.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}
##papasout_2.0_10.root           : {'good': True, 'n_events': 100000L, 'zero_size': False}'''
##        self.assertMultiLineEqual(str(dataset),printout)



if __name__ == '__main__':
    unittest.main()
