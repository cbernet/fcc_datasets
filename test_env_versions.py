import unittest

from fcc_datasets.env_versions import EnvVersions

########################################################################
class TestEnvVersion(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.env_versions =EnvVersions({'podio':"PODIO",
                                        'dag':"FCCDAG", 
                                        'junk':'FCCJUNK', 
                                        'root':'ROOTSYS'
                                        'papas':'FCCPAPASCPP'})
        print self.env_versions

    #----------------------------------------------------------------------
    def test_1_yaml(self):
        """"""
        fname = 'software.yaml'
        self.env_versions.write_yaml(fname)
        import yaml
        with open(fname) as infile:
            data = yaml.load(infile)
            for package in self.env_versions.tracked :
                info = self.env_versions.tracked[package]
                if isinstance(info, dict) and 'commitid' in info:
                    info = info['commitid']           
                self.assertEqual(data['software'][package],info)
        
        
if __name__ == '__main__':
    unittest.main()

