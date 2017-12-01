import unittest
import tempfile
import copy
import os
import shutil

do_test = True    
try:
    import heppy
except ImportError:
    do_test = False
    
if do_test:
    from heppy.test.plot_ee_b import Plotter
    from heppy.framework.looper import Looper
    from ROOT import TFile
    if 'FCCDATASETBASEOUT' in os.environ:
        del os.environ['FCCDATASETBASEOUT']
    
    from analysis_test_cfg import config
    
    import logging
    logging.getLogger().setLevel(logging.ERROR)
    
    import heppy.statistics.rrandom as random
    
    class TestAnalysis(unittest.TestCase):
    
        def setUp(self):
            os.environ['FCCDATASETBASEOUT'] = os.path.abspath('test')                    
            random.seed(0xdeadbeef)
            self.outdir = tempfile.mkdtemp()
            import logging
            logging.disable(logging.CRITICAL)
    
        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)
    
        def test_1(self):
            '''Check the analysis runs'''
            from heppy.papas.detectors.CMS import cms
            config.components[0].splitFactor = 1
            self.looper = Looper( self.outdir, config,
                                  nEvents=100,
                                  nPrint=0 )
            self.looper.loop()
            self.looper.write()    

if __name__ == '__main__':

    unittest.main()
