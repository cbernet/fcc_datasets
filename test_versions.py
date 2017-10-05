import unittest

scriptfname = 'data/analysis_ee_ZH_nunubb_cfg.py'
from versions import Versions

########################################################################
class TestVersion(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        self.versions = Versions(scriptfname, ['heppy', 'fcc_ee_higgs'])
        print self.versions

    #----------------------------------------------------------------------
    def test_1(self):
        """"""
        pass
    
        
        
##if __name__ == '__main__':
##    unittest.main()
