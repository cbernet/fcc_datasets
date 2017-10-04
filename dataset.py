import basedir

import glob
import os
import pprint
import shelve
import copy
from ROOT import TFile


class File(object):

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path) 
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
        return tree.GetEntries()
        
    def __str__(self):
        return '{:<30} : {}'.format(self.name, pprint.pformat(self.flags))
        

class Directory(object):

    def __init__(self, path):
        self.path = path

    def abspath(self, fname):
        return '/'.join([self.path, fname])


class Dataset(Directory):

    def __init__(self, name, pattern='*.root', cache=True):
        self.name = name
        if cache: 
            self._read_from_cache()
        else:
            self.path = basedir.abspath(name)
            self.all_files = dict()
            self.good_files = dict()
            self._build_list_of_files(pattern)
            self._write_to_cache()

    def _build_list_of_files(self, pattern):
        for path in glob.glob(self.abspath(pattern)):
            the_file = File(path)
            self.all_files[the_file.name] = the_file
            if the_file.good():
                self.good_files[the_file.name] = the_file
        
    def nfiles(self):
        '''return the total number of files, good or not'''
        return len(self.all_files)

    def ngoodfiles(self):
        """return the number of good files."""
        return len(self.good_files)
            
    def list_of_good_files(self):
        return [the_file.path for the_file in self.all_files.values() if the_file.good()]

    def nevents(self):
        '''Returns the sum of the number of events in all good files'''
        return sum([f.nevents() for f in self.good_files.values()])

    def _read_from_cache(self):
        sh = shelve.open(self._cache_fname())
        self.__dict__ = copy.deepcopy(sh['dataset'].__dict__)
        sh.close()
        
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
        return '\n'.join(lines)
        
