import unittest
import os
from condor_parameters import CondorParameters, setup_condor_parser

########################################################################
class TestCondorParameters(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def setUp(self):
        """"""
        parser = setup_condor_parser()
        (options,args) = parser.parse_args()
        if len(args) != 0:
            parser.print_usage()
            sys.exit(1)

            #extract options and create condor_parameters class to hold the run parameters
            #this will also construct a unique subdirectory name
        self.condor_parameters = CondorParameters(options)

    #----------------------------------------------------------------------
    def test_1_yaml(self):
        """"""
        self.condor_parameters.write_yaml(os.getcwd())
        condor_pars= CondorParameters("parameters.yaml")
        for thing in ("base_outputdir", "name", "input", "script", "events", "runs", "subdirectory"):
            self.assertEqual(condor_pars[thing],self.condor_parameters[thing])
        os.remove("parameters.yaml")
        
        
if __name__ == '__main__':
    unittest.main()

