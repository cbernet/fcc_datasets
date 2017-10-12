import unittest
import os

import basedir

# basedir.basename = os.path.abspath('test')
# basedir.basecache = os.path.abspath('test/.fcc_datasets')

def abspath(name):
    return '/'.join([basedir.basename, name])
dataset_name_fccsw = 'papas/ee_to_ZZ_condor_A_703'
dataset_name_heppy = 'heppy/papas/ee_to_ZZ_condor_A_703'
cfg_name = abspath('analysis_test_cfg.py')
dataset_pattern_fccsw = '*.root'
dataset_pattern_heppy = 'heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root'

from fcc_datasets.dataset import Dataset
from fcc_datasets.fcc_component import FCCComponent

cache = False

class TestFccswDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw,
                               cache=False,
                               xsection=1.8e-9)
        self.nfiles = 10
        self.ngoodfiles = 10
        self.nevents = 10

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files), self.nfiles)
        self.assertEqual(len(self.dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(self.dataset.nfiles(), self.nfiles)
        self.assertEqual(self.dataset.ngoodfiles(), self.ngoodfiles)

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name_fccsw, cache=cache)
        self.assertEqual(len(dataset.all_files), self.nfiles)
        self.assertEqual(len(dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name_fccsw, cache=cache)
        self.assertEqual(dataset.nevents(), 100)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name_fccsw, cache=cache)
        data_written = dataset.write_yaml()
        data_read = dataset._read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_fccsw(self):
        """test that the jobtype can be determined for fccsw"""
        dataset = Dataset(dataset_name_fccsw, cache=cache)
        self.assertEqual(dataset._jobtype, 'fccsw')

    #----------------------------------------------------------------------
    def test_6_update(self):
        """test that when something is changed, the unique id stays the same.
        """
        dataset = Dataset(dataset_name_fccsw, xsection=1, cache=True)
        self.assertEqual(dataset.uid(), self.dataset.uid())
        self.assertEqual(dataset.xsection(), 1)
        dataset = Dataset(dataset_name_fccsw, cache=True)
        self.assertEqual(dataset.xsection(), 1)
         
        
class TestHeppyDataset(unittest.TestCase):
    
    def setUp(self):
        self.dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy,
                               cache=False,
                               cfg=cfg_name, xsection=1.8e-9)        
        self.nfiles = 1
        self.ngoodfiles = 1
        self.nevents = 100

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files), self.nfiles)
        self.assertEqual(len(self.dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(self.dataset.nfiles(), self.nfiles)
        self.assertEqual(self.dataset.ngoodfiles(), self.ngoodfiles)

    def test_2_cache(self):
        '''Test dataset reading from cache'''
        dataset = Dataset(dataset_name_heppy, cache=True)
        self.assertEqual(len(dataset.all_files), self.nfiles)
        self.assertEqual(len(dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name_heppy, cache=True)
        self.assertEqual(dataset.nevents(), self.nevents)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy, 
                          cache=cache)
        data_written = dataset.write_yaml()
        data_read = dataset._read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_heppy(self):
        """test that the jobtype can be determined for heppy"""
        dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy, 
                          cache=cache)
        self.assertEqual(dataset._jobtype, 'heppy')
    
        
class TestFCCComponent(unittest.TestCase):
    
    #----------------------------------------------------------------------
    def test_1(self):
        """Test FCC component creation"""
        dset = Dataset(dataset_name_fccsw, cache=cache)
        comp = FCCComponent(dataset_name_fccsw, dataset_pattern_fccsw,
                            xsection=dset.xsection())
        self.assertListEqual(dset.list_of_good_files(),
                             comp.files)
        self.assertEqual(dset.xsection(),
                         comp.xSection)
        print comp
        
        
        
        
##    def test_3_print(self):
##        dataset = Dataset(dataset_name, dataset_pattern, cache=cache)
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
