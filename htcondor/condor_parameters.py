import os
import pprint
import fnmatch
import re
import git
import yaml
import sys
import fnmatch
from filename_handler import FilenameHandler
import datetime
import optparse 



########################################################################
class CondorParameters(object):
    """
    creates a dict of condor run parameters
    """

    #----------------------------------------------------------------------
    #def __init__(self, options):
        #self.pars = dict()
        #self.add("eosdir",options.eosdir)
        #self.add("input",FilenameHandler(options.input))
        #self.add("script",FilenameHandler(options.script)) 
        #self.add("nevents",int(options.nevents))
        #self.add("runs",int(options.runs) )   
        #self.add("subdirectory",self.get_next_condor_directory())
        
    def __init__(self, inputs):
        #parameters can arrive from options
        if isinstance(inputs, optparse.Values):
           self.pars = dict() 
           self.add("eosdir",inputs.eosdir)
           self.add("input",inputs.input)
           self.add("script",inputs.script) 
           self.add("nevents",int(inputs.nevents))
           self.add("runs",int(inputs.runs) )   
           self.add("subdirectory",self.get_next_condor_directory())
        else:   #or from a yaml file with a parameters section
            with open(inputs, mode='r') as infile:
                self.pars = yaml.load(infile)["parameters"]
            
    
    def add(self, key, value):
        self.pars[key] = value
        
    def __getitem__(self, index):
        return self.pars[index]
    
    #----------------------------------------------------------------------
    def write_yaml(self, path, filename ="parameters.yaml"):
        '''write the versions to a yaml file'''
        outfile = '/'.join([path, filename])
        data = dict(parameters=dict())
        # write out either the directory or the git commit if this was found
        for key, value in self.pars.iteritems():
            #if hasattr(value,"__str__"):
            #    data['parameters'][key] = value.__str__()
            #else:
                data['parameters'][key] = value
        with open(outfile, mode='w') as outfile:
                yaml.dump(data, outfile,
                          default_flow_style=False)   
                
    def get_next_condor_directory(self, basename=None):
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
