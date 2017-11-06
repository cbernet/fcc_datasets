import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from condor_parameters import CondorParameters
import optparse 

'''Finish.py produces a summary output yaml file which will contain details of the root files in the output directory and will
amalgamate all other yaml files'''

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
        
    #read in the condor parameters from parameters.yaml so that we know the location of the output directory
    print " read condor pars "
    condor_pars= CondorParameters("parameters.yaml")
    
    #this is the directory where the root files are stored
    outdir = '/'.join((condor_pars["base_outputdir"],condor_pars["subdirectory"]))
    #create a touch file (will be removed at the end if everything works)
    filename= '/'.join((outdir ,"finish.txt"))
    print outdir
    os.system("touch "+ filename)
    curdir = os.getcwd()
    
    #move to the output directory
    os.chdir(condor_pars["base_outputdir"])
    
    '''base directory where outputs are stored'''
    basedir.basename = condor_pars["base_outputdir"]

    #process the root files and other yaml files
    process_dataset(condor_pars["subdirectory"], options)
    print "ls"
    os.system("ls -al " +  outdir)
    
    #remove the touch file
    os.system("rm "+ filename)
    
    #move back to the original directory
    os.chdir(curdir)
    print "finished creation of info.yaml"
