import unittest

scriptfname = 'test/cfg_test_versions.py'
from fcc_datasets.versions import Versions

########################################################################
class TestVersion(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.versions = Versions(scriptfname, ['fcc_datasets'])

    #----------------------------------------------------------------------
    def test_1_yaml(self):
        """"""
        fname = 'software.yaml'
        self.versions.write_yaml(fname)
        import yaml
        with open(fname) as infile:
            data = yaml.load(infile)
            self.assertEqual(data['software']['fcc_datasets'],
                             self.versions.tracked['fcc_datasets']['commitid'])
        
        
if __name__ == '__main__':
    unittest.main()

