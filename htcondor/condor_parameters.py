import os
import pprint
import yaml
import sys
from fcc_datasets.htcondor.filename_handler import FilenameHandler
import datetime
import optparse 


def setup_condor_parser():
    ''' Reads in options from the line command line:
    The options are
    -p parameters -b base_outputdir -i inputfile -s script -e nevents -r runs
    '''
    from optparse import OptionParser
    #defaults are in FCCDATASETS directory
    environ = os.environ
    datasetsdir = ""
    eosdir=""
    if "FCCDATASETS" in environ:
        datasetsdir = environ["FCCDATASETS"] 
    else:
        print "FCCDATASETS environment variable is missing - call init.sh"
    if "EOSCONDOR" in environ:
        eosdir = environ["EOSCONDOR"] 
    else:
        print "EOSCONDOR environment variable is missing - call/read init.sh"    
        
    parser = OptionParser(
        usage='%prog  [options]',
        description='set up ready for condor dag run'
    ) 
    parser.add_option(
        "-p","--parameters", dest="parameters",
        default="scripts/papas_parameters.yaml",
        help="default model parameters yaml"
    )    
    parser.add_option(
        "-b","--base_outputdir", dest="base_outputdir",
        help="directory for outputs"
    )
    parser.add_option(
        "-i","--input" ,dest="input",
        help="input file"
    )    
    parser.add_option(
        "-s","--script", dest="script",
        help="fccsw script to run"
    ) 
    parser.add_option(
        "-e","--nevents", dest="nevents",
        help="number of events"
    ) 
    parser.add_option(
        "-r","--runs", dest="runs",
        help="number of htcondor runs"
    )         
    return parser


class CondorParameters(object): 
    """
    creates a dict of condor run parameters either using command line options
    or reading in from an existing parameters.yaml file.
    The parameters can also be written to a parameters.yaml file.
    """
        
    def __init__(self, inputs):
        #parameters can arrive from options
        if isinstance(inputs, optparse.Values):
            pardict= vars(inputs)
            with open(inputs.parameters, mode='r') as infile:
                self.pars = yaml.load(infile)["default_parameters"]            
            for key, value in pardict.iteritems():
                if value:
                    try:
                        self.add(key,int(value))
                    except:
                        self.add(key,value) 
            self.add("subdirectory",self._get_next_condor_directory())
        else:   #or from a yaml file with a parameters section
            with open(inputs, mode='r') as infile:
                self.pars = yaml.load(infile)["parameters"]

    def add(self, key, value):
        self.pars[key] = value
        
    def __getitem__(self, index):
        return self.pars[index]
    
    def write_yaml(self, path, filename ="parameters.yaml"):
        '''write the condor parameters to a yaml file'''
        outfile = '/'.join([path, filename])
        data = dict(parameters=dict())
        
        for key, value in self.pars.iteritems():
                data['parameters'][key] = value
        with open(outfile, mode='w') as outfile:
                yaml.dump(data, outfile,
                          default_flow_style=False)   
                
    def _get_next_condor_directory(self, basename=None):
        ''' make a new directory name of the form condor_basename_20171019_e10_r3_uniqueid '''
        if basename is None:
            basename = FilenameHandler(self.pars["input"]).core()
        dt=datetime.datetime.now().strftime('%Y%m%d')    
        subdirectory='_'.join(("condor", basename, dt, "e" +str(self["nevents"]), "r"+str(self["runs"])))
    
        #automatically number the directory so it is unique
        x=0
        while os.path.isdir('_'.join((subdirectory, str(x)))):
            x= x+1
        outdir = '_'.join((subdirectory, str(x)))  
        return outdir    

    def __str__(self):
        return pprint.pformat(self.pars)
