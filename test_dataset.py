import unittest
import os

import fcc_datasets.basedir as basedir
basedir.set_basename()

def abspath(name):
    return '/'.join([basedir.basename(), name])
dataset_name_fccsw = 'papas/ee_to_ZZ_condor_A_703'
dataset_name_heppy = 'heppy/papas/ee_to_ZZ_condor_A_703'
dataset_name_pythia8 = 'pythia/ee_Z_ddbar'
cfg_name = abspath('analysis_test_cfg.py')
dataset_pattern_fccsw = '*.root'
dataset_pattern_heppy = 'heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root'
dataset_pattern_pythia8 = 'Job*/*.root'

from fcc_datasets.dataset import Dataset, Directory

cache = False

class TestFccswDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset(dataset_name_fccsw,
                               dataset_pattern_fccsw,
                               extract_info=True, 
                               cache=False,
                               xsection=1.8e-9)
        self.dataset.write()
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
        dataset = Dataset(dataset_name_fccsw, cache=True)
        self.assertEqual(len(dataset.all_files), self.nfiles)
        self.assertEqual(len(dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(dataset.uid(), self.dataset.uid())

    #----------------------------------------------------------------------
    def test_3_nevents(self):
        """Test that the number of events is correct"""
        dataset = Dataset(dataset_name_fccsw, cache=True)
        self.assertEqual(dataset.nevents(), 100)

    #----------------------------------------------------------------------
    def test_4_yaml(self):
        """Test that the yaml file can be written and read."""
        dataset = Dataset(dataset_name_fccsw, cache=True)
        data_written = dataset._write_yaml()
        data_read = dataset._read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_fccsw(self):
        """test that the jobtype can be determined for fccsw"""
        dataset = Dataset(dataset_name_fccsw, cache=True)
        self.assertEqual(dataset.jobtype(), 'fccsw')

    #----------------------------------------------------------------------
    def test_6_update(self):
        """test that when something is changed, the unique id stays the same.
        """
        dataset = Dataset(dataset_name_fccsw, xsection=1, cache=True)
        self.assertEqual(dataset.uid(), self.dataset.uid())
        self.assertEqual(dataset.xsection(), 1)
        dataset.write()
        dataset = Dataset(dataset_name_fccsw, cache=True)
        self.assertEqual(dataset.xsection(), 1)
    
    def test_empty(self):
        """Check that an exception is raised when trying to
        read a dataset with no root file"""
        with self.assertRaises(ValueError):
            dataset = Dataset('papas/empty_dataset', '*.root', extract_info=True)
    
    def test_no_good_root_file(self):
        with self.assertRaises(ValueError):
            dataset = Dataset('papas/nogood_dataset', '*.root', extract_info=True)
        
    def test_no_yaml(self):
        with self.assertRaises(IOError):
            dataset = Dataset('papas/empty_dataset', '*.root', extract_info=False)
        
class TestHeppyDataset(unittest.TestCase):
    
    def setUp(self):
        self.dataset = Dataset(dataset_name_heppy, dataset_pattern_heppy,
                               cache=False,
                               extract_info=True, 
                               cfg=cfg_name, xsection=1.8e-9)
        self.dataset.write()
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
        data_written = dataset._write_yaml()
        data_read = dataset._read_yaml()
        self.assertDictEqual(data_written, data_read)
        
    #----------------------------------------------------------------------
    def test_5_jobtype_heppy(self):
        """test that the jobtype can be determined for heppy"""
        dataset = Dataset(dataset_name_heppy,
                          dataset_pattern_heppy, 
                          cache=False,
                          extract_info=True)
        self.assertEqual(dataset.jobtype(), 'heppy')
    
        
class TestPythia8Dataset(unittest.TestCase):
    
    def setUp(self):
        self.dataset = Dataset(dataset_name_pythia8, dataset_pattern_pythia8,
                               cache=False,
                               extract_info=True, 
                               cfg=cfg_name, xsection=1.8e-9)        
        self.dataset.write()
        self.nfiles = 5
        self.ngoodfiles = 5
        self.nevents = 50

    def test_1_create(self):
        '''Test dataset creation'''
        self.assertEqual(len(self.dataset.all_files), self.nfiles)
        self.assertEqual(len(self.dataset.list_of_good_files()), self.ngoodfiles)
        self.assertEqual(self.dataset.nfiles(), self.nfiles)
        self.assertEqual(self.dataset.ngoodfiles(), self.ngoodfiles)
        self.assertEqual(self.dataset.nevents(), self.nevents)
        self.assertEqual(self.dataset.jobtype(), 'pythia8')

do_test = True      
try:
    import heppy
except ImportError:
    do_test = False
if do_test:
    from fcc_datasets.fcc_component import FCCComponent       
    class TestFCCComponent(unittest.TestCase):
           
        #----------------------------------------------------------------------
        def test_1(self):
            """Test FCC component creation"""
            dset = Dataset(dataset_name_fccsw, dataset_pattern_fccsw,
                           cache=False)
            comp = FCCComponent(dataset_name_fccsw, 
                                xSection=dset.xsection())
            self.assertListEqual(dset.list_of_good_files(),
                                 comp.files)

        
##class TestDirectory(unittest.TestCase):
##    
##    def test_1(self):
##        directory = Directory('A/B')
##        self.assertEqual(directory.relpath('foo/bar.root'),
##                         'foo/bar.root')
##        
        
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
