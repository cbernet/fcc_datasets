
if __name__ == '__main__':   
    import unittest
    import sys
    import os
    import fcc_datasets

    os.environ['FCCDATASETS'] = '/'.join([fcc_datasets.__path__[0],
                                          'test'])

    os.chdir(fcc_datasets.__path__[0])

    suites = []
    
    pcks = [
        '.', 
        ]

    for pck in pcks:
        loader =  unittest.TestLoader()
        suites.append(loader.discover(pck))

    suite = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

 


