#!/usr/bin/env python 
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir

def process_dataset(dsname, options):
    ds = Dataset(dsname,
                 pattern=options.wildcard,
                 extract_info=options.extract, 
                 xsection=options.xsection, 
                 cache=False)
    ds.write()
    if options.verbose:
        print ds
    else:
        print dsname

if __name__ == '__main__':
    
    import sys
    import os
    from optparse import OptionParser
    import fcc_datasets
    
    parser = OptionParser(
        usage='%prog <dataset_name> [options]',
        description='publish a dataset'
    )    
    parser.add_option(
        "-w","--wildcard", dest="wildcard",
        default="*.root",
        help="wildcard to select files in the dataset"
    )    
    parser.add_option(
        "-b","--basedir", dest="basedir",
        default=basedir.basename(),
        help="base directory containing all samples."
    )    
    parser.add_option(
        "-v","--verbose", dest="verbose",
        default=False,
        action="store_true", 
        help="print information."
    )    
    parser.add_option(
        "-x","--xsection", dest="xsection", type=float, 
        default=None,
        help="cross section to be assigned to the sample."
    )    
    parser.add_option(
        "-e","--extract", dest="extract",
        default=False,
        action="store_true", 
        help="extract meta information from the dataset."
    )    
    (options,args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)
        
    dsname = args[0]
    basedir.set_basename(options.basedir)
    
    process_dataset(dsname, options)
