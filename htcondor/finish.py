import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from condor_parameters import CondorParameters
import optparse 

'''Finish.py produces a summary output yaml file which will contain details of the root files in the output directory and will
amalgamate all other yaml files'''

if __name__ == '__main__':
    
    
    #read in the condor parameters from parameters.yaml so that we know the location of the output directory
    condor_pars= CondorParameters("parameters.yaml")
    
    #this is the directory where the root files are stored
    outdir = '/'.join((condor_pars["base_outputdir"],condor_pars["subdirectory"]))
    
    #create a touch file (will be removed at the end if everything works)
    filename= '/'.join((outdir ,"finish.txt"))
    os.system("touch "+ filename)
    curdir = os.getcwd()
    
    #move to the output directory
    os.chdir(condor_pars["base_outputdir"])
    
    '''base directory where outputs are stored'''
    basedir.set_basename(condor_pars["base_outputdir"])
    ds = Dataset(condor_pars["subdirectory"],
                     pattern="*.root",
                     xsection=None,
                     extract_info=True,
                     cache=False)
    ds.write()
    
    print "ls"
    os.system("ls -al " +  outdir)
    #put a copy of inf.yaml in the work directory for easy reference
    os.system("cp " + condor_pars["subdirectory"] +"/info.yaml " + curdir  )
    
    #remove the touch file
    os.system("rm "+ filename)
    
    #move back to the original directory
    os.chdir(curdir)
    print "finished creation of info.yaml"
