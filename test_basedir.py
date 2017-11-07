import unittest
import os

import fcc_datasets.basedir as basedir
import fcc_datasets

class TestBaseDir(unittest.TestCase):
    
    def test_1(self):
        os.environ['FCCDATASETBASEOUT'] = 'blah'
        self.assertEqual(basedir.basename(),
                         'blah')        
        del os.environ['FCCDATASETBASEOUT']
        self.assertEqual(basedir.basename(),
                         '/'.join([fcc_datasets.__path__[0], 'test']))
        basedir.set_basename('foo')
        self.assertEqual(basedir.basename(),
                         'foo')
        os.environ['FCCDATASETBASEOUT'] = 'bar'       
        self.assertEqual(basedir.basename(),
                         'bar')
        import test.setbasedir
        self.assertEqual(basedir, test.setbasedir.basedir)
        self.assertEqual(basedir.basename(), 'foobar')
       
    def tearDown(self):
        basedir.set_basename()
       
if __name__ == '__main__':
    unittest.main()
