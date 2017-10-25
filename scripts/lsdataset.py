#!/usr/bin/env python 
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir

def process_dataset(dsname, options):
    ds = Dataset(dsname)
    print ds

if __name__ == '__main__':
    
    import sys
    import os
    from optparse import OptionParser
    import fcc_datasets
    
    parser = OptionParser(
        usage='%prog <dataset_name> [options]',
        description='list a dataset'
    )    
    parser.add_option(
        "-b","--basedir", dest="basedir",
        default=basedir.basename,
        help="base directory containing all samples."
    )    
    (options,args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)
        
    dsname = args[0]
    basedir.basename = options.basedir
    
    process_dataset(dsname, options)
