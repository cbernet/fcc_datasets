#!/bin/bash


import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from condor_parameters import CondorParameters
import optparse 


if __name__ == '__main__':
    
    from optparse import OptionParser
    
    
    parser = OptionParser(
                          usage='%prog  cluster job ',
                          description='do a condor run'
                          )
    
    (options,args) = parser.parse_args()
    
    if len(args) != 2:
        parser.print_usage()
        sys.exit(1)
    
    job=sys.argv[2]
    
    condor_pars= CondorParameters("parameters.yaml")
    
    outdir = '/'.join((condor_pars["eosdir"],condor_pars["subdirectory"]))
    #todo format
    print "do gaudi run"
    filename= outdir + "/" + "run_" + job + ".root"
    os.system("touch "+ filename)
    
    print "do gaudi run"
    
