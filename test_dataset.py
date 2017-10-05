import unittest
import os
import basedir
from dataset import Dataset
from fcc_component import FCCComponent

if not os.path.isdir(basedir.basename):
    basedir.basename = os.path.abspath('test')
dataset_name_fccsw = 'papas/ee_to_ZZ_1oct_A_1'
dataset_name_heppy = 'heppy/ee_to_ZZ_1oct_A_1'
cfg_name = 'test/analysis_test_cfg.py'
dataset_pattern_fccsw = '*.0_1*.root'
dataset_pattern_heppy = 'heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root'

class TestFccswDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw,
                               cache=False,
                               xsection=1.8e-9)        

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files),11)
        self.assertEqual(len(self.dataset.list_of_good_files()),9)
        self.assertEqual(self.dataset.nfiles(), 11)
        self.assertEqual(self.dataset.ngoodfiles(), 9)
        self.dataset.write_yaml()

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw, cache=True)
        self.assertEqual(len(dataset.all_files),11)
        self.assertEqual(len(dataset.list_of_good_files()),9)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw, cache=True)
        self.assertEqual(dataset.nevents(), 900000)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw, cache=True)
        data_written = dataset.write_yaml()
        data_read = dataset.read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_fccsw(self):
        """test that the jobtype can be determined for fccsw"""
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw, cache=False)
        self.assertEqual(dataset._jobtype, 'fccsw')
        
        
class TestHeppyDataset(unittest.TestCase):
    
    def setUp(self):
        self.dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy,
                               cache=False,
                               cfg=cfg_name, xsection=1.8e-9)        

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files), 1)
        self.assertEqual(len(self.dataset.list_of_good_files()), 1)
        self.assertEqual(self.dataset.nfiles(), 1)
        self.assertEqual(self.dataset.ngoodfiles(), 1)

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy, cache=True)
        self.assertEqual(len(dataset.all_files),1)
        self.assertEqual(len(dataset.list_of_good_files()), 1)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy, cache=True)
        self.assertEqual(dataset.nevents(), 45000)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy, cache=True)
        data_written = dataset.write_yaml()
        data_read = dataset.read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_heppy(self):
        """test that the jobtype can be determined for heppy"""
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_heppy, cache=False)
        self.assertEqual(dataset._jobtype, 'heppy')
    
        
class TestFCCComponent(unittest.TestCase):
    
    #----------------------------------------------------------------------
    def test_1(self):
        """Test FCC component creation"""
        dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw, cache=True)
        comp = FCCComponent(dataset_name_fccsw, dataset_pattern_fccsw)
        self.assertListEqual(dataset.list_of_good_files(),
                             comp.files)
        self.assertEqual(dataset._xsection,
                         comp.xSection)
        print comp
        
        
        
        
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
