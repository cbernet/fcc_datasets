import unittest
import os
import random
from fcc_datasets.dataset import Dataset

class TestPublish(unittest.TestCase):
    
    #----------------------------------------------------------------------
    def test_1_publish(self):
        """Test that the publish script is working."""
        xsection = random.uniform(0, 1)
        dsname = 'heppy/papas/ee_to_ZZ_condor_A_703' 
        cmd = 'python publish.py {} -x {}'.format(
            dsname, 
            xsection
        )
        os.system(cmd)        
        dset = Dataset(dsname)
        self.assertAlmostEqual(dset.xsection(), xsection, places=7)

if __name__ == '__main__':
    unittest.main()
