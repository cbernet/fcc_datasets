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
    print "start gaudi run"

    gaudi_command = 'LD_PRELOAD=$FCCSWBASEDIR/build.$BINARY_TAG/lib/libPapasUtils.so $FCCSWBASEDIR/run  fccrun.py {}  --rpythiainput  {} --routput output.root  --rmaxevents {}'.format(                                                                                                                                                    condor_pars["script"], condor_pars["input"], int(condor_pars["nevents"]))
    print gaudi_command
    os.system(gaudi_command)
    move_command = 'xrdcp output.root {}/{}/output_{}.root'.format( condor_pars["eosdir"], condor_pars["subdirectory"], job)
    print move_command
    os.system(move_command)
    #os.system("touch "+ filename)
    
    print "finish gaudi run"
    
