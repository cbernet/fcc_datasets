

import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from condor_parameters import CondorParameters
import optparse 

def process_dataset(dsname, options):
    '''Process the directory containing output files and write summary information to info.yaml'''
    ds = Dataset(dsname,
                 pattern=options.wildcard,
                 xsection=options.xsection,
                 cache=False)
    ds.write()


if __name__ == '__main__':
    
    from optparse import OptionParser
    
    
    parser = OptionParser(
                          usage='%prog [options]',
                          description='finish a condor run'
                          )
    parser.add_option(
        "-b","--basedir", dest="basedir",
        default=basedir.basename,
        help="base directory containing all samples."
    )    
    
    parser.add_option(
                      "-w","--wildcard", dest="wildcard",
                      default="*.root",
                      help="wildcard to select files in the dataset"
                      )
    parser.add_option(
        "-x","--xsection", dest="xsection", type=float, 
        default=None,
        help="cross section to be assigned to the sample."
    )    
    
    (options,args) = parser.parse_args()
    
    if len(args) != 0:
        parser.print_usage()
        sys.exit(1)
        
    
    condor_pars= CondorParameters("parameters.yaml")
    
    outdir = '/'.join((condor_pars["eosdir"],condor_pars["subdirectory"]))
    filename= '/'.join((outdir ,"papasfinish.txt"))
    os.system("touch "+ filename)
    
    '''base directory where outputs are stored'''
    basedir.basename = condor_pars["eosdir"]
    process_dataset(condor_pars["subdirectory"], options)
    print "ls"
    os.system("ls -al " +  outdir)
    os.system("rm "+ filename)
    print "finished creation of info.yaml"
