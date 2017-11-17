import fcc_datasets.basedir as basedir
from versions import Versions

import glob
import os
import pprint
import dill
import pickle
import shelve
import copy
import datetime
import yaml
import uuid
import re
import sys
from ROOT import TFile


class File(object):

    def __init__(self, path, dataset_path):
        self.path = path
        self.name = os.path.basename(path)
        self.rel_path = path.replace(dataset_path, "").strip('/')
        self._check()

    def good(self):
        '''is the file good?'''
        return self.flags['good']
    
    def nevents(self):
        '''return the number of events.'''
        return self.flags['n_events']

    def _check(self):
        self.flags = dict()
        to_check = ['zero_size', 
                    'n_events']
        for testname in to_check:
            method = getattr(self, '_check_{}'.format(testname))
            self.flags[testname] = method()
        self.flags['good'] = not self.flags['zero_size']

    def _check_zero_size(self):
        statinfo = os.stat(self.path)
        return statinfo.st_size==0

    def _check_n_events(self):
        if self.flags['zero_size']:
            return None
        rootfile = TFile(self.path)
        tree = rootfile.Get("events")
        return int(tree.GetEntries())
        
    def __str__(self):
        return '{:<30} : {}'.format(self.rel_path, pprint.pformat(self.flags))
        

class Directory(object):

    def __init__(self, name):
        self.path = basedir.abspath(name)

    def abspath(self, fname):
        return '/'.join([self.path, fname])        


class Dataset(Directory):

    def __init__(self, name, pattern=None,
                 extract_info=False, 
                 cache=True,
                 cfg=None, xsection=None):
        super(Dataset, self).__init__(name)
        self.name = name
        # self._pattern = pattern
        # self._uid = None
        # self._mother = None
        # self._versions = None
        ##        self._jobtype = None
        self._data = {
            "sample": {
                "mother": None,
                "jobtype": None,
                "pattern": pattern,
            },
            "software": {},
        }
        
        self._info_fname = self.abspath('info.yaml')
        cache_read = False
        if cache:
            cache_read = self._read_from_cache()
        change_requested = pattern or cfg or xsection \
            or not cache or not cache_read
        if change_requested:
            self._xsection = xsection
            # self._build_list_of_files()
            if extract_info:
                self.extract_info()
            else:
                self.load_info()
            if not os.path.isdir(self.path):
                raise ValueError('{} does not exist, check your base sample directory'.format(self.path))

            
    def uid(self):
        return self._data['sample'].get('id', None)
    
    #----------------------------------------------------------------------
    def extract_info(self):
        """"""
        self._build_list_of_files()
        self._guess_jobtype()
        self._find_mother()
        self._aggregate_yaml()
        if self.uid() is None:
            self._data['sample']['id'] = uuid.uuid4()
                
    def load_info(self):
        data = self._read_yaml()
        self._data.update(data)
        self._build_list_of_files()        

    #----------------------------------------------------------------------
##    def _analyze_cfg(self, cfgname):
##        """Analyze the cfg used to build the dataset.
##        get the commit ids of the relevant imported packages
##        possibly find the mother sample(s)? 
##        """
##        self._versions = Versions(cfgname, ['heppy',
##                                            'fcc_ee_higgs',
##                                            'fcc_datasets']).tracked

    #----------------------------------------------------------------------
    def _guess_jobtype(self):
        pattern = re.compile('(\S*\D)(\d+)\.root$')
        indices = []
        prefix = []
        jobtype = None
        for fname in self.list_of_good_files():
            fname = os.path.basename(fname)
            m = pattern.match(fname)
            if m:
                prefix.append(m.group(1))
                indices.append(int(m.group(2)))
        if len(set(prefix)) == 1 and len(indices):
            #same prefix, several indices
            jobtype = 'fccsw'
        pattern = re.compile('\S*\S+\.\S+\.\S+\_\d+\/\S+\.root$')
        for fname in self.list_of_good_files():
            m = pattern.match(fname)
            if m:
                jobtype = 'heppy'
        pattern = re.compile('^Job_\S+\/\S+.root$')
        match = []
        for fname in self.all_files:
            m = pattern.match(fname)
            if m:
                match.append(fname)
        if len(match) == len(self.all_files):
            jobtype = 'pythia8'
        self._data['sample']['jobtype'] = jobtype

    #----------------------------------------------------------------------
    def _find_mother(self):
        """find the mother dataset and store its name in _mother"""
        if self.jobtype() == 'heppy':
            # load config from pickle file and get the mother from the input component
            sys.path.insert(0, self.path)
            with open(self.abspath('component.pck')) as config_file:
                comp = pickle.load(config_file)
                mother_name = comp['name'].split('_Chunk')[0]
                self._data['sample']['mother'] = mother_name
                

    #----------------------------------------------------------------------
    def _aggregate_yaml(self):
        """Retrieve info from existing yaml files in the dataset directory.
        Do not consider the main yaml file of the dataset in case it
        already exists. 
        """
        yaml_files = glob.glob(self.abspath('*.yaml'))
        for yfile in yaml_files:
            if yfile == self._info_fname:
                continue
            data = self._read_yaml(yfile)
            self._data.update(data)
        

    #----------------------------------------------------------------------
    def _build_list_of_files(self):
##        if not self._pattern:
##            self._pattern = self._data['pattern']
        self.all_files = dict()
        self.good_files = dict()        
        abspattern = self.abspath( self._data['sample']['pattern'] )
        for path in glob.glob(abspattern):
            the_file = File(path, self.path)
            self.all_files[the_file.rel_path] = the_file
            if the_file.good():
                self.good_files[the_file.rel_path] = the_file
        if len(self.all_files) == 0:
            raise ValueError('no file matching {}'.format(abspattern))
        if len(self.good_files) == 0:
            raise ValueError('no good root file matching {}'.format(abspattern))
        self._data['sample']['ngoodfiles'] = len(self.good_files)
        self._data['sample']['nfiles'] = len(self.all_files)
        self._data['sample']['nevents'] = self.nevents()
        
        
    #----------------------------------------------------------------------
    def list_of_good_files(self):
        good_files = []
        for key, the_file in sorted(self.all_files.iteritems()):
            if the_file.good():
                good_files.append(the_file.path) 
        return good_files

    def nfiles(self):
        '''return the total number of files, good or not'''
        return len(self.all_files)

    def ngoodfiles(self):
        """return the number of good files."""
        return len(self.good_files)

    def nevents(self):
        '''Returns the sum of the number of events in all good files'''
        return sum([f.nevents() for f in self.good_files.values()])

    def jobtype(self):
        '''Returns the type of jobs used to produce the dataset:
        "fcssw", "heppy", None
        '''
        return self._data['sample']['jobtype']
    
    def xsection(self):
        '''Returns the cross-section'''
        return self._xsection

    def mother(self):
        '''Returns the mother'''
        return self._data['sample']['mother']

    #----------------------------------------------------------------------
    def write(self):
        """"""
        self._write_to_cache()
        self._write_yaml()
        

    #----------------------------------------------------------------------
    def _write_yaml(self):
        '''write the yaml file'''
##        self._data['sample'] = {
##            'name': self.name,
##            'pattern': self._pattern,
##            # 'id': self.uid(),
##            # 'jobtype': self.jobtype(),
##            # 'mother' : self.mother(),
##            'nevents': self.nevents(),
##            'njobs': self.nfiles(),
##            'njobs_ok': self.ngoodfiles(),
##            'user': os.environ['USER'],
##            'timestamp': datetime.datetime.now().isoformat(),
##            'xsection': self._xsection,
##        }
##        if self._versions:
##            software_data = dict()
##            for key, info in self._versions.iteritems():
##                software_data[key] = str(info['commitid'])
##            self.data['software'] = software_data
##        if os.path.isfile(self._info_fname):
##            with open(self._info_fname) as infile:
##                old_data = yaml.load(infile)             
        with open(self._info_fname, mode='w') as outfile:
                yaml.dump(self._data, outfile,
                          default_flow_style=False)
        return self._data  
            
    #----------------------------------------------------------------------
    def _read_yaml(self, fname=None):
        if fname is None:
            fname = self._info_fname
        with open(fname, mode='r') as infile:
            data = yaml.load(infile)
            return data
    
    #----------------------------------------------------------------------
    def _read_from_cache(self):
        fname = self._cache_fname()
        if not os.path.isfile(fname):
            return False
        sh = shelve.open(fname)
        try:
            dataset = sh['dataset']
            # self.__dict__ = copy.deepcopy(dataset.__dict__)
            self.__dict__.update(dataset.__dict__)
        except ImportError as err:
            raise
        finally:
            sh.close()
        return True
        
    #----------------------------------------------------------------------
    def _write_to_cache(self):
        cache = basedir.abscache(self.name)
        if not os.path.isdir(cache):
            os.makedirs(cache)
        sh = shelve.open(self._cache_fname())
        sh['dataset'] = self
        sh.close()

    def _cache_fname(self):
        cache = basedir.abscache(self.name)
        return '/'.join([cache,'cache.shv'])

    def __str__(self):
        lines = [self.name]
        lines.append(self.path)
        files = map(str, self.all_files.values())
        lines.extend(files)
        lines.append(pprint.pformat(self._data))
        return '\n'.join(lines)
    
    def __repr__(self):
        return self.name
        
