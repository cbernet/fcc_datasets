import unittest

scriptfname = 'test/analysis_test_cfg.py'
from fcc_datasets.versions import Versions

########################################################################
class TestVersion(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.versions = Versions(scriptfname, ['heppy', 'fcc_ee_higgs'])
        print self.versions

    #----------------------------------------------------------------------
    def test_1_yaml(self):
        """"""
        fname = 'software.yaml'
        self.versions.write_yaml(fname)
        import yaml
        with open(fname) as infile:
            data = yaml.load(infile)
            self.assertEqual(data['software']['heppy'],
                             self.versions.tracked['heppy']['commitid'])
        
        
if __name__ == '__main__':
    unittest.main()

